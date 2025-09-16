from urllib.parse import quote_plus
from sqlmodel import create_engine, Session, SQLModel
from dotenv import load_dotenv
import os
from sqlalchemy.orm import declarative_base

Base = declarative_base()

load_dotenv()

DB_USER = os.getenv("DATABASE_USERNAME")
DB_PASS = quote_plus(os.getenv("DATABASE_PASSWORD"))  # encode special chars
DB_HOST = os.getenv("DATABASE_HOST")
DB_PORT = os.getenv("DATABASE_PORT")
DB_NAME = os.getenv("DATABASE_NAME")
DB_CHARSET = os.getenv("DATABASE_CHARSET", "utf8mb4")

DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset={DB_CHARSET}"

engine = create_engine(DB_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def test_connection():
    from sqlalchemy import text
    try:
        with Session(engine) as session:
            session.exec(text("SELECT 1"))
        print("Database connection successful")
    except Exception as e:
        print("Database connection failed:", e)
