from app.core.security import hash_password, verify_password


def test_hash_password_does_not_store_plaintext() -> None:
    password = "correct-horse-battery-staple"

    hashed = hash_password(password)

    assert hashed != password


def test_verify_password_accepts_correct_password() -> None:
    password = "correct-horse-battery-staple"
    hashed = hash_password(password)

    assert verify_password(password, hashed)


def test_verify_password_rejects_incorrect_password() -> None:
    password = "correct-horse-battery-staple"
    hashed = hash_password(password)

    assert not verify_password("wrong-password", hashed)


def test_same_password_produces_different_hashes() -> None:
    password = "correct-horse-battery-staple"

    first_hash = hash_password(password)
    second_hash = hash_password(password)

    assert first_hash != second_hash
