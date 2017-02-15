from sqlalchemy import create_engine, Integer, Column, String
from sqlalchemy.ext.declarative import declarative_base

db_uri = 'sqlite:///db/db.sqlite'
engine = create_engine(db_uri)

Base = declarative_base()


class Notice(Base):
    __tablename__ ='notice'
    id = Column(Integer, primary_key=True)
    name = Column(String(10))
    num = Column(Integer)


Base.metadata.create_all(bind=engine)

