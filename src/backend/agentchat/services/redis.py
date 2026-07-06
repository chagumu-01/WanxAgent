import pickle
import redis
from loguru import logger
from typing import Optional
from agentchat.settings import app_settings
from redis import ConnectionPool, RedisCluster
from redis.backoff import ExponentialBackoff
from redis.cluster import ClusterNode
from redis.retry import Retry
from redis.sentinel import Sentinel

class RedisClient:
    
    def __init__(self, url, max_connections=10):
        if isinstance(url, str):
            try:
                self.pool = ConnectionPool.from_url(url, max_connections=max_connections)
                self.connection = redis.StrictRedis(connection_pool=self.pool)
                self.connection.ping()
                logger.info("Redis connection successful")
                self.use_local_cache = False
            except Exception as e:
                logger.warning(f"Redis connection failed, using local cache instead: {e}")
                from agentchat.services.local_cache import LocalCacheClient
                self.local_cache = LocalCacheClient()
                self.use_local_cache = True
        else:
            logger.error(f"redis init only support Standalone mode")

    def cluster_nodes(self, key):
        if isinstance(self.connection,
                      RedisCluster) and self.connection.get_default_node() is None:
            target = self.connection.get_node_from_key(key)
            self.connection.set_default_node(target)

    def setNx(self, key, value, expiration=3600):
        if self.use_local_cache:
            return self.local_cache.setNx(key, value, expiration)
        try:
            if pickled := pickle.dumps(value):
                result = self.connection.setnx(key, pickled)
                self.connection.expire(key, expiration)
                if not result:
                    return False
                return True
        except TypeError as exc:
            raise TypeError('RedisCache only accepts values that can be pickled. ') from exc
        finally:
            self.close()

    def set(self, key, value, expiration=3600):
        if self.use_local_cache:
            return self.local_cache.set(key, value, expiration)
        try:
            if pickled := pickle.dumps(value):
                result = self.connection.setex(key, expiration, pickled)
                if not result:
                    raise ValueError('redis could not set value')
            else:
                logger.error('pickle error, value={}', value)
        except TypeError as exc:
            raise TypeError('RedisCache only accepts values that can be pickled. ') from exc
        finally:
            self.close()

    def hsetkey(self, name, key, value, expiration=3600):
        if self.use_local_cache:
            return self.local_cache.hsetkey(name, key, value, expiration)
        try:
            r = self.connection.hset(name, key, value)
            if expiration:
                self.connection.expire(name, expiration)
            return r
        finally:
            self.close()

    def hset(self, name,
             key: Optional[str] = None,
             value: Optional[str] = None,
             mapping: Optional[dict] = None,
             items: Optional[list] = None,
             expiration: int = 3600):
        if self.use_local_cache:
            return self.local_cache.hset(name, key, value, mapping, items, expiration)
        try:
            r = self.connection.hset(name, key, value, mapping, items)
            if expiration:
                self.connection.expire(name, expiration)
            return r
        finally:
            self.close()

    def hget(self, name, key):
        if self.use_local_cache:
            return self.local_cache.hget(name, key)
        try:
            return self.connection.hget(name, key)
        finally:
            self.close()

    def hgetall(self, name):
        if self.use_local_cache:
            return self.local_cache.hgetall(name)
        try:
            return self.connection.hgetall(name)
        finally:
            self.close()

    def delete(self, key):
        if self.use_local_cache:
            return self.local_cache.delete(key)
        try:
            return self.connection.delete(key)
        finally:
            self.close()

    def get(self, key):
        if self.use_local_cache:
            return self.local_cache.get(key)
        try:
            value = self.connection.get(key)
            return pickle.loads(value) if value else None
        finally:
            self.close()

    def incr(self, key, expiration=3600):
        if self.use_local_cache:
            return self.local_cache.incr(key, expiration)
        try:
            value = self.connection.incr(key)
            if expiration:
                self.connection.expire(key, expiration)
            return value
        finally:
            self.close()

    def close(self):
        if not self.use_local_cache:
            self.connection.close()

# 实例化对象
redis_client = RedisClient(app_settings.redis.get('endpoint'))