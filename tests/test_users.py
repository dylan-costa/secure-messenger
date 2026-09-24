def test_create_user_succeeds(client):
    response = client.post("/users", json={"username": "alice", "password": "pw12345"})

    assert response.status_code == 200
    body = response.json()
    assert body["username"] == "alice"
    assert body["keys"] == []


def test_create_user_duplicate_username_returns_409(client):
    client.post("/users", json={"username": "alice", "password": "pw12345"})

    response = client.post("/users", json={"username": "alice", "password": "different"})

    assert response.status_code == 409


def test_get_user_not_found_returns_404(client):
    response = client.get("/users/nobody")

    assert response.status_code == 404


def test_add_user_key_appears_on_get_user(client):
    created = client.post("/users", json={"username": "bob", "password": "pw12345"}).json()

    response = client.post(
        f"/users/{created['id']}/keys",
        json={"method": "RSA", "public_key_json": '{"e":"65537","n":"123"}'},
    )

    assert response.status_code == 200
    assert response.json()["keys"] == [{"method": "RSA", "public_key_json": '{"e":"65537","n":"123"}'}]

    fetched = client.get("/users/bob").json()
    assert fetched["keys"][0]["method"] == "RSA"


def test_add_user_key_for_unknown_user_returns_404(client):
    response = client.post(
        "/users/999999/keys",
        json={"method": "RSA", "public_key_json": "{}"},
    )

    assert response.status_code == 404


def test_adding_second_key_for_same_method_replaces_it(client):
    created = client.post("/users", json={"username": "dana", "password": "pw12345"}).json()

    client.post(f"/users/{created['id']}/keys", json={"method": "RSA", "public_key_json": '{"n":"1"}'})
    response = client.post(f"/users/{created['id']}/keys", json={"method": "RSA", "public_key_json": '{"n":"2"}'})

    keys = response.json()["keys"]
    assert len(keys) == 1
    assert keys[0]["public_key_json"] == '{"n":"2"}'
