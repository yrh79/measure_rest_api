import logging
import sys

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy import (Column,
                        Integer,
                        String,
                        ForeignKey,
                        JSON,
                        Sequence,
                        DateTime,
                        Text,
                        UniqueConstraint,
                        Index,
                       )
from sqlalchemy.dialects.mysql import INTEGER

from sqlalchemy.orm import relationship, backref

BaseModel = declarative_base()

class dataVal(BaseModel):
    __tablename__ = 'vol_curr'

    id = Column(Integer, primary_key=True, autoincrement=True)
    voltage = Column(Integer, nullable=True)
    current = Column(Integer, nullable=True)
    ts = Column(DateTime, nullable=True)

    def __str__(self):
        return "volCurrData"

