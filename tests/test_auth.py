def test_login_succeeds_with_correct_credentials(client):
    client.post("/users", json={"username": "carol", "password": "pw12345"})

    response = client.post("/login", json={"username": "carol", "password": "pw12345"})

    assert response.status_code == 200
    assert response.json()["username"] == "carol"


def test_login_fails_with_wrong_password(client):
    client.post("/users", json={"username": "carol", "password": "pw12345"})

    response = client.post("/login", json={"username": "carol", "password": "wrong"})

    assert response.status_code == 401


def test_login_fails_for_unknown_user(client):
    response = client.post("/login", json={"username": "ghost", "password": "whatever"})

    assert response.status_code == 401


def test_login_response_includes_uploaded_keys(client):
    created = client.post("/users", json={"username": "erin", "password": "pw12345"}).json()
    client.post(f"/users/{created['id']}/keys", json={"method": "ECC", "public_key_json": '{"x":1,"y":2}'})

    response = client.post("/login", json={"username": "erin", "password": "pw12345"})

    assert response.json()["keys"] == [{"method": "ECC", "public_key_json": '{"x":1,"y":2}'}]
