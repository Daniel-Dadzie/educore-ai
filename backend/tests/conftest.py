import os
from collections.abc import Generator
from pathlib import Path

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

import app.models  # noqa: F401
from app.db.base import Base
from app.db.session import get_db
from app.main import app

TEST_ENV_FILE = Path(__file__).with_name(".env.test")
load_dotenv(TEST_ENV_FILE)


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
        join_transaction_mode="create_savepoint",
    )

    session = session_factory()

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def client(db_session: Session) -> Generator[TestClient, None, None]:
    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
