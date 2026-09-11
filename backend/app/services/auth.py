from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User
from app.repositories.users import get_user_by_email


class EmailAlreadyRegisteredError(Exception):
    pass


def register_user(
    db: Session,
    *,
    email: str,
    password: str,
    first_name: str,
    last_name: str,
) -> User:
    normalized_email = email.strip().lower()

    existing_user = get_user_by_email(db, normalized_email)

    if existing_user is not None:
        raise EmailAlreadyRegisteredError

    user = User(
        email=normalized_email,
        password_hash=hash_password(password),
        first_name=first_name.strip(),
        last_name=last_name.strip(),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
