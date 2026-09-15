import re

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.enums import Role
from app.models.membership import OrganizationMember
from app.models.organization import Organization
from app.models.user import User
from app.repositories.users import get_user_by_email


class EmailAlreadyRegisteredError(Exception):
    pass


class RegistrationConflictError(Exception):
    pass


def _slugify(value: str) -> str:
    normalized = value.strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", normalized)
    return slug.strip("-")[:100]


def register_user(
    db: Session,
    *,
    email: str,
    password: str,
    first_name: str,
    last_name: str,
    organization_name: str,
) -> User:
    normalized_email = email.strip().lower()
    normalized_first_name = first_name.strip()
    normalized_last_name = last_name.strip()
    normalized_organization_name = organization_name.strip()
    organization_slug = _slugify(normalized_organization_name)

    existing_user = get_user_by_email(db, normalized_email)

    if existing_user is not None:
        raise EmailAlreadyRegisteredError

    user = User(
        email=normalized_email,
        password_hash=hash_password(password),
        first_name=normalized_first_name,
        last_name=normalized_last_name,
    )

    organization = Organization(
        name=normalized_organization_name,
        slug=organization_slug,
    )

    membership = OrganizationMember(
        organization=organization,
        user=user,
        role=Role.STUDENT,
    )

    db.add(user)
    db.add(organization)
    db.add(membership)

    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise RegistrationConflictError from exc

    db.refresh(user)

    return user
