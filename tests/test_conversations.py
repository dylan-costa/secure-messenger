import json


def _create_two_users(client, name1="userA", name2="userB"):
    a = client.post("/users", json={"username": name1, "password": "pw12345"}).json()
    b = client.post("/users", json={"username": name2, "password": "pw12345"}).json()
    return a["id"], b["id"]


def test_create_rsa_conversation_has_no_domain_params(client):
    a_id, b_id = _create_two_users(client)

    response = client.post(
        "/conversations", json={"user1_id": a_id, "user2_id": b_id, "encryption_method": "RSA"}
    )

    assert response.status_code == 200
    body = response.json()
    assert body["encryption_method"] == "RSA"
    assert body["domain_params_json"] is None


def test_create_ecc_conversation_generates_domain_params(client):
    a_id, b_id = _create_two_users(client)

    response = client.post(
        "/conversations", json={"user1_id": a_id, "user2_id": b_id, "encryption_method": "ECC"}
    )

    assert response.status_code == 200
    params = json.loads(response.json()["domain_params_json"])
    assert set(params.keys()) == {"p", "a", "b", "gx", "gy"}


def test_create_conversation_is_idempotent_for_same_pair(client):
    a_id, b_id = _create_two_users(client)

    first = client.post(
        "/conversations", json={"user1_id": a_id, "user2_id": b_id, "encryption_method": "RSA"}
    ).json()
    second = client.post(
        "/conversations", json={"user1_id": a_id, "user2_id": b_id, "encryption_method": "ECC"}
    ).json()

    # A second POST for the same pair returns the EXISTING conversation
    # rather than creating a competing one under a different method.
    assert second["id"] == first["id"]
    assert second["encryption_method"] == "RSA"


def test_lookup_conversation_404_when_none_exists(client):
    a_id, b_id = _create_two_users(client)

    response = client.get(f"/conversations/lookup/{a_id}/{b_id}")

    assert response.status_code == 404


def test_lookup_conversation_finds_existing_regardless_of_argument_order(client):
    a_id, b_id = _create_two_users(client)
    created = client.post(
        "/conversations", json={"user1_id": a_id, "user2_id": b_id, "encryption_method": "RSA"}
    ).json()

    response = client.get(f"/conversations/lookup/{b_id}/{a_id}")

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_add_conversation_key_rejects_non_participant(client):
    a_id, b_id = _create_two_users(client)
    outsider = client.post("/users", json={"username": "outsider", "password": "pw12345"}).json()
    conv = client.post(
        "/conversations", json={"user1_id": a_id, "user2_id": b_id, "encryption_method": "ECC"}
    ).json()

    response = client.post(
        f"/conversations/{conv['id']}/keys",
        json={"user_id": outsider["id"], "public_key_json": "{}"},
    )

    assert response.status_code == 400


def test_add_conversation_key_succeeds_for_participant(client):
    a_id, b_id = _create_two_users(client)
    conv = client.post(
        "/conversations", json={"user1_id": a_id, "user2_id": b_id, "encryption_method": "ECC"}
    ).json()

    response = client.post(
        f"/conversations/{conv['id']}/keys",
        json={"user_id": a_id, "public_key_json": '{"x":1,"y":2}'},
    )

    assert response.status_code == 200
    keys = response.json()["keys"]
    assert len(keys) == 1
    assert keys[0]["user_id"] == a_id


def test_get_conversation_by_id_not_found_returns_404(client):
    response = client.get("/conversations/999999")

    assert response.status_code == 404
