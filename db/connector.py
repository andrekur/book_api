from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

USER = 'test_user'
PASSWORD = 'test_user'
HOST = 'localhost'
PORT = 5433
DB = 'api_dev'

engine = create_engine(
    f'postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}')

Session = sessionmaker(autocommit=False, autoflush=True, bind=engine)

Base = declarative_base()
