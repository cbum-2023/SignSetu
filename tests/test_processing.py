import pytest

from conftest import assert_known_bug


@pytest.mark.contract
def test_process_video_returns_accepted(client, token, created_video):
    response = client.process_video(created_video["id"], token=token)

    assert response.status_code == 202, response.text


@pytest.mark.known_bug
def test_duplicate_processing_request_is_rejected(client, token, created_video, strict_known_bugs):
    video_id = created_video["id"]

    first = client.process_video(video_id, token=token)
    second = client.process_video(video_id, token=token)

    assert first.status_code == 202, first.text
    assert_known_bug(
        second.status_code in {400, 409},
        f"Expected duplicate processing request to be rejected, got {second.status_code}: {second.text}",
        strict_known_bugs,
    )
