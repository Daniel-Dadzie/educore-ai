import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.enums import Role
from app.models.membership import OrganizationMember
from app.models.organization import Organization
from app.models.user import User
from app.services.auth import (
    EmailAlreadyRegisteredError,
    RegistrationConflictError,
    register_user,
)


def test_register_user_creates_user_organization_and_student_membership(
    db_session: Session,
) -> None:
    user = register_user(
        db_session,
        email=" Daniel@Example.com ",
        password="CorrectHorseBatteryStaple!",
        first_name=" Daniel ",
        last_name=" Dadzie ",
        organization_name="EduCore University",
    )

    assert user.email == "daniel@example.com"
    assert user.first_name == "Daniel"
    assert user.last_name == "Dadzie"
    assert user.password_hash != "CorrectHorseBatteryStaple!"
    assert user.password_hash.startswith("$argon2id$")

    organization = db_session.scalar(
        select(Organization).where(
            Organization.slug == "educore-university",
        )
    )

    assert organization is not None
    assert organization.name == "EduCore University"

    membership = db_session.scalar(
        select(OrganizationMember).where(
            OrganizationMember.user_id == user.id,
            OrganizationMember.organization_id == organization.id,
        )
    )

    assert membership is not None
    assert membership.role == Role.STUDENT


def test_register_user_rejects_duplicate_email(
    db_session: Session,
) -> None:
    register_user(
        db_session,
        email="daniel@example.com",
        password="CorrectHorseBatteryStaple!",
        first_name="Daniel",
        last_name="Dadzie",
        organization_name="EduCore University",
    )

    with pytest.raises(EmailAlreadyRegisteredError):
        register_user(
            db_session,
            email="DANIEL@example.com",
            password="AnotherStrongPassword!",
            first_name="Another",
            last_name="User",
            organization_name="Another University",
        )


def test_registration_rolls_back_on_database_conflict(
    db_session: Session,
) -> None:
    register_user(
        db_session,
        email="first@example.com",
        password="CorrectHorseBatteryStaple!",
        first_name="First",
        last_name="User",
        organization_name="EduCore University",
    )

    with pytest.raises(RegistrationConflictError):
        register_user(
            db_session,
            email="second@example.com",
            password="AnotherStrongPassword!",
            first_name="Second",
            last_name="User",
            organization_name="EduCore University",
        )

    second_user = db_session.scalar(
        select(User).where(User.email == "second@example.com")
    )

    assert second_user is None
