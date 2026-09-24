def _create_two_users(client):
    a = client.post("/users", json={"username": "sender1", "password": "pw12345"}).json()
    b = client.post("/users", json={"username": "receiver1", "password": "pw12345"}).json()
    return a["id"], b["id"]


def test_send_message_stores_ciphertext_verbatim(client):
    sender_id, receiver_id = _create_two_users(client)

    response = client.post(
        "/messages",
        json={
            "sender_id": sender_id,
            "receiver_id": receiver_id,
            "ciphertext": "999888777",
            "ciphertext_for_sender": "111222333",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["ciphertext"] == "999888777"
    assert body["ciphertext_for_sender"] == "111222333"


def test_send_message_links_to_existing_conversation(client):
    sender_id, receiver_id = _create_two_users(client)
    client.post(
        "/conversations",
        json={"user1_id": sender_id, "user2_id": receiver_id, "encryption_method": "RSA"},
    )

    response = client.post(
        "/messages", json={"sender_id": sender_id, "receiver_id": receiver_id, "ciphertext": "abc"}
    )

    assert response.json()["conversation_id"] is not None


def test_send_message_without_a_conversation_still_succeeds(client):
    sender_id, receiver_id = _create_two_users(client)

    response = client.post(
        "/messages", json={"sender_id": sender_id, "receiver_id": receiver_id, "ciphertext": "abc"}
    )

    assert response.status_code == 200
    assert response.json()["conversation_id"] is None


def test_send_message_with_unknown_sender_returns_400_not_500(client):
    _, receiver_id = _create_two_users(client)

    response = client.post(
        "/messages", json={"sender_id": 999999, "receiver_id": receiver_id, "ciphertext": "abc"}
    )

    assert response.status_code == 400


def test_send_message_with_unknown_receiver_returns_400_not_500(client):
    sender_id, _ = _create_two_users(client)

    response = client.post(
        "/messages", json={"sender_id": sender_id, "receiver_id": 999999, "ciphertext": "abc"}
    )

    assert response.status_code == 400


def test_get_conversation_history_orders_by_timestamp(client):
    sender_id, receiver_id = _create_two_users(client)
    client.post("/messages", json={"sender_id": sender_id, "receiver_id": receiver_id, "ciphertext": "first"})
    client.post("/messages", json={"sender_id": receiver_id, "receiver_id": sender_id, "ciphertext": "second"})

    response = client.get(f"/conversations/{sender_id}/{receiver_id}")

    assert response.status_code == 200
    assert [m["ciphertext"] for m in response.json()] == ["first", "second"]
