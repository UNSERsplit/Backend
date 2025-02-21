import os
from sqlmodel import create_engine, Session

from typing import Annotated
from fastapi import Depends

engine = create_engine(os.environ["DB_URL"])


def _get_db():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()

DB = Annotated[Session, Depends(_get_db)]
