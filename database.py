from sqlalchemy import Column, Integer,String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine=create_engine('sqlite:///database1.db', connect_args={"check_same_thread": False})
Base=declarative_base()
Sessionlocal=sessionmaker(autoflush=False, autocommit=False,bind=engine)
session_local=Sessionlocal

