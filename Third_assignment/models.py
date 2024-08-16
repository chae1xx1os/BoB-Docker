from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

Base = declarative_base()

class User(Base):
    __tablename__ = "user_table"

    user_id = Column(String(50), primary_key=True, index=True)

class Access(Base):
    __tablename__ = "access_table"

    access_id = Column(String(50), primary_key=True, index=True)
    user_id = Column(String(50), index=True)
    channel_id = Column(String(50))
    access_time = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class IoC(Base):
    __tablename__ = "ioc_table"

    id = Column(String(50), primary_key=True, index=True)
    indicator = Column(String(255), nullable=False)
    ioc_type = Column(String(50), nullable=False)
    description = Column(String(255))
    last_seen = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class Friend(Base):
    __tablename__ = "friends"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    specialty = Column(String(100))
    description = Column(String(255))
