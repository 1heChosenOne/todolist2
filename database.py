from sqlalchemy import create_engine, text

engine=create_engine('sqlite:///database1.db', echo=True, connect_args={"check_same_thread": False})

