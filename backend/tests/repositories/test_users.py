from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.users import get_user_by_email


def test_get_user_by_email_returns_user(db_session: Session) -> None:
    user = User(
        email="daniel@example.com",
        password_hash="test-hash",
        first_name="Daniel",
        last_name="Dadzie",
    )

    db_session.add(user)
    db_session.flush()

    result = get_user_by_email(
        db_session,
        "daniel@example.com",
    )

    assert result is not None
    assert result.id == user.id
    assert result.email == "daniel@example.com"


def test_get_user_by_email_returns_none_when_not_found(
    db_session: Session,
) -> None:
    result = get_user_by_email(
        db_session,
        "missing@example.com",
    )

    assert result is None


def test_get_user_by_email_does_not_match_different_email(
    db_session: Session,
) -> None:
    user = User(
        email="daniel@example.com",
        password_hash="test-hash",
        first_name="Daniel",
        last_name="Dadzie",
    )

    db_session.add(user)
    db_session.flush()

    result = get_user_by_email(
        db_session,
        "another@example.com",
    )

    assert result is None
