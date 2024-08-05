from sqlalchemy import Column, String, DateTime
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
