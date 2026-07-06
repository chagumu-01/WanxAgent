import logging

from contextlib import contextmanager, asynccontextmanager
from typing import Iterator, AsyncIterator

from sqlmodel import Session
from agentchat.database import engine

logger = logging.getLogger(__name__)

@contextmanager
def session_getter() -> Iterator[Session]:
    session = Session(engine)

    try:
        yield session
    except Exception as e:
        logger.info('Session rollback because of exception:{}', e)
        session.rollback()
        raise
    finally:
        session.close()

class AsyncSessionWrapper:
    def __init__(self, session: Session):
        self.session = session

    async def exec(self, statement):
        return self.session.exec(statement)

    async def get(self, model, id):
        return self.session.get(model, id)

    async def commit(self):
        self.session.commit()

    async def refresh(self, instance):
        self.session.refresh(instance)

    def add(self, instance):
        self.session.add(instance)

    def delete(self, instance):
        self.session.delete(instance)

    def close(self):
        self.session.close()

@asynccontextmanager
async def async_session_getter() -> AsyncIterator[AsyncSessionWrapper]:
    session = Session(engine)
    wrapper = AsyncSessionWrapper(session)

    try:
        yield wrapper
    except Exception as e:
        logger.info('Session rollback because of exception: %s', e)
        session.rollback()
        raise
    finally:
        session.close()