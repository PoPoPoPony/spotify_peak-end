import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


DB_NAME = os.getenv("POSTGRE_NAME")
DB_PWD = os.getenv("POSTGRE_PWD")
# SQLALCHEMY_DATABASE_URL = "postgresql://" + DB_NAME + ":"+  DB_PWD +"@127.0.0.1:5432/postgres"
# SQLALCHEMY_DATABASE_URL = "postgresql://" + "postgres" + ":"+  "pony5487" +"@172.19.0.3:5432/postgres"
SQLALCHEMY_DATABASE_URL = "postgresql://" + "postgres" + ":"+  "pony5487" +"@postgres/postgres"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
