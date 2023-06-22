from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from nbaplayers.config import DevelopmentConfig

def create_db_schema(engine):
    Base.metadata.create_all(engine)

db_connection = DevelopmentConfig.SQLALCHEMY_DATABASE_URI

engine = create_engine(db_connection)
Session = sessionmaker(bind=engine)

Base = declarative_base()
