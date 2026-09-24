#Database connection and setup

import os

from sqlalchemy import create_engine #database connection
from sqlalchemy.orm import sessionmaker, declarative_base


# Locally this defaults to the SQLite dev file. In production (Render), the
# DATABASE_URL env var points at a real Postgres instance instead. Render's
# connection strings use the legacy "postgres://" scheme; SQLAlchemy 2.x
# requires "postgresql://", so it's rewritten here rather than in every place
# that reads the env var.
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./secure_messenger.db")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# check_same_thread is a SQLite-only connect arg -- passing it to the
# Postgres driver would raise a TypeError.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args
) #connect to the database



SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #create a session

# Database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base = declarative_base() #create a base class for the models

