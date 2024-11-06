from functools import lru_cache
from typing import Iterator

from sqlalchemy.orm import Session

from fastapi_utils.session import FastAPISessionMaker

from app.core.config import settings


def get_db() -> Iterator[Session]:
    """FastAPI dependency that provides a sqlalchemy session"""
    yield from _get_fastapi_sessionmaker().get_db()


@lru_cache()
def _get_fastapi_sessionmaker() -> FastAPISessionMaker:
    """This function could be replaced with a global variable if preferred"""
    return FastAPISessionMaker(settings.SQLALCHEMY_DATABASE_URI.unicode_string())
