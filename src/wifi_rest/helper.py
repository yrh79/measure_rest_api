import logging

from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from db_models import *


connstr_engine_map = {}


def get_sql_engine(conn_str):
    engine = connstr_engine_map.get(conn_str, None)
    if engine is None:
        engine = create_engine(conn_str, echo=False, pool_size=2)
        connstr_engine_map[conn_str] = engine
    return engine


class ConnStrDBSession(object):
    def __init__(self, connstr):
        self.connstr = connstr

    def __enter__(self):
        self.engine = get_sql_engine(self.connstr)
        self._session_factory = scoped_session(sessionmaker(bind=self.engine, autoflush=False))
        self._session = self._session_factory()
        return self._session

    def __exit__(self, *exc):
        self._session.close()
        self._session_factory.remove()
        return False

