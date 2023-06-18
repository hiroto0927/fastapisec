from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()


HOST = os.environ.get("HOST")
USERS = os.environ.get("USERS")
PASS = os.environ.get("PASS")
POSTGRES_DB = os.environ.get("POSTGRES_DB")

DATABASE_URL = "postgresql://{}:{}@{}/{}".format(USERS, PASS, HOST, POSTGRES_DB)

engine = create_engine(DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
