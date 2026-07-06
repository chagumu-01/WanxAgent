import pickle
import time
from loguru import logger
from typing import Optional


class LocalCacheClient:
    def __init__(self):
        self.cache = {}
        self.expirations = {}
        logger.info("Local cache initialized")

    def _clean_expired(self):
        now = time.time()
        expired_keys = [key for key, exp in self.expirations.items() if exp < now]
        for key in expired_keys:
            del self.cache[key]
            del self.expirations[key]

    def setNx(self, key, value, expiration=3600):
        self._clean_expired()
        if key in self.cache:
            return False
        try:
            self.cache[key] = pickle.dumps(value)
            self.expirations[key] = time.time() + expiration
            return True
        except TypeError as exc:
            raise TypeError('LocalCache only accepts values that can be pickled. ') from exc

    def set(self, key, value, expiration=3600):
        self._clean_expired()
        try:
            self.cache[key] = pickle.dumps(value)
            self.expirations[key] = time.time() + expiration
        except TypeError as exc:
            raise TypeError('LocalCache only accepts values that can be pickled. ') from exc

    def hsetkey(self, name, key, value, expiration=3600):
        self._clean_expired()
        if name not in self.cache:
            self.cache[name] = {}
        self.cache[name][key] = value
        self.expirations[name] = time.time() + expiration
        return 1

    def hset(self, name,
             key: Optional[str] = None,
             value: Optional[str] = None,
             mapping: Optional[dict] = None,
             items: Optional[list] = None,
             expiration: int = 3600):
        self._clean_expired()
        if name not in self.cache:
            self.cache[name] = {}
        if mapping:
            self.cache[name].update(mapping)
        elif key is not None and value is not None:
            self.cache[name][key] = value
        elif items:
            for k, v in items:
                self.cache[name][k] = v
        self.expirations[name] = time.time() + expiration
        return len(self.cache[name])

    def hget(self, name, key):
        self._clean_expired()
        if name in self.cache and key in self.cache[name]:
            return self.cache[name][key]
        return None

    def hgetall(self, name):
        self._clean_expired()
        return self.cache.get(name, {})

    def delete(self, key):
        self._clean_expired()
        if key in self.cache:
            del self.cache[key]
            del self.expirations[key]
            return 1
        return 0

    def get(self, key):
        self._clean_expired()
        if key in self.cache:
            try:
                return pickle.loads(self.cache[key])
            except (pickle.UnpicklingError, EOFError):
                return None
        return None

    def incr(self, key, expiration=3600):
        self._clean_expired()
        if key not in self.cache:
            self.cache[key] = 0
        self.cache[key] += 1
        self.expirations[key] = time.time() + expiration
        return self.cache[key]

    def close(self):
        pass