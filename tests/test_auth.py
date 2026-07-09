def test_authentication(client):
    
    response = client.auth()

    assert response.status_code == 201

    data = response.json()

    assert "token" in data
    assert "expiresAt" in data