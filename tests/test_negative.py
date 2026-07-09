import time

import pytest
import requests


@pytest.mark.negative
def test_missing_candidate_header_returns_client_error(base_url):
    response = requests.post(f"{base_url}/api/auth", timeout=10)

    assert response.status_code in {400, 401}, response.text


@pytest.mark.negative
@pytest.mark.slow
def test_expired_token_is_rejected(client, token):
    create = client.create_video(token=token)
    assert create.status_code == 201, create.text
    video_id = create.json()["id"]

    time.sleep(6)

    response = client.get_video(
        video_id,
        token=token,
    )

    assert response.status_code == 401, response.text


@pytest.mark.negative
def test_invalid_video_id_returns_not_found_or_bad_request(client, token):
    response = client.get_video("invalid-video-id", token=token)

    assert response.status_code in {400, 404}, response.text


@pytest.mark.negative
def test_process_nonexistent_video_returns_not_found(client, token):
    response = client.process_video("fake-video-id", token=token)

    assert response.status_code in {400, 404}, response.text
