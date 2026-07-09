import pytest


@pytest.mark.contract
def test_authentication_returns_token_and_expiry(client):
    response = client.auth()

    assert response.status_code == 201, response.text
    data = response.json()
    assert data["token"]
    assert data["expiresAt"]


@pytest.mark.known_bug
def test_same_candidate_can_reauthenticate(client, strict_known_bugs):
    first = client.auth()
    second = client.auth()

    assert first.status_code == 201, first.text
    from conftest import assert_known_bug

    assert_known_bug(
        second.status_code == 201,
        f"Expected re-authentication to issue a fresh token, got {second.status_code}: {second.text}",
        strict_known_bugs,
    )
