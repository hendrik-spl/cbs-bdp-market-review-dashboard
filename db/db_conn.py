# This file is used to store all functionality related to the database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DATABASE_URI
from contextlib import contextmanager

# Create a connection to the database
engine = create_engine(DATABASE_URI)

# Create a base class for the ORM
Base = declarative_base()

# Create a session class to interact with the database
Session = sessionmaker(bind = engine)

@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

def ping_db(engine):
    # Test connection to the database
    try:
        conn = engine.connect()
        return True
    except Exception as e:
        print(e)
        return False