from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

database_host = 'postgresql://user:password@localhost:5432/univer_postgre'
engine = create_engine(database_host, echo=False)  
DBSession = sessionmaker(bind=engine)
session = DBSession()
