from server.services import password_services


def test_hash_password_does_not_store_plaintext():
    hashed = password_services.hash_password("mysecret123")
    assert hashed != "mysecret123"


def test_verify_password_accepts_correct_password():
    hashed = password_services.hash_password("mysecret123")
    assert password_services.verify_password("mysecret123", hashed) is True


def test_verify_password_rejects_wrong_password():
    hashed = password_services.hash_password("mysecret123")
    assert password_services.verify_password("wrongpassword", hashed) is False
