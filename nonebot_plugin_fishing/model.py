from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class FishingRecord(Base):
    __tablename__ = "fishing_record"

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    time = Column(Integer)
    frequency = Column(Integer)


class FishingBackpack(Base):
    __tablename__ = "fishing_backpack"

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    fishes = Column(String)
