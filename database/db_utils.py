import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def get_env_var(var_name: str):
    """
    A function for safely obtaining an environment variable. If specified env is not exist raise EnvironmentError

    :param var_name: name of the environment variable
    :return: value of environment variable if it exists
    """
    value = os.getenv(var_name)
    if value is None:
        raise EnvironmentError(f'Missing required environment variable: {var_name}')
    return value


DB_USER = get_env_var('DB_USER')
DB_PASSWORD = get_env_var('DB_PASSWORD')
DB_NAME = get_env_var('DB_NAME')
DB_HOST = get_env_var('DB_HOST')

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@/{DB_NAME}?host={DB_HOST}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, isolation_level="READ UNCOMMITTED")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def create_schema():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()