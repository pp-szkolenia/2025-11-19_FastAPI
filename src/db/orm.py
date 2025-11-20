from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from db.utils import get_connection_string


connection_string = get_connection_string()
engine = create_engine(connection_string)
SessionLocal = sessionmaker(engine, future=True)


class Base(DeclarativeBase):
    pass


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
