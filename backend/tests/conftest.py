import os
from collections.abc import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

import app.models  # noqa: F401
from app.db.base import Base


@pytest.fixture(scope="session")
def test_engine():
    database_url = os.environ["TEST_DATABASE_URL"]

    engine = create_engine(
        database_url,
        pool_pre_ping=True,
    )

    Base.metadata.create_all(bind=engine)

    yield engine

    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture
def db_session(test_engine) -> Generator[Session, None, None]:
    connection = test_engine.connect()
    transaction = connection.begin()

    session_factory = sessionmaker(
        bind=connection,
        class_=Session,
        autoflush=False,
        autocommit=False,
    )

    session = session_factory()

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()
