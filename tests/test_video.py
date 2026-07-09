import pytest

from conftest import assert_known_bug


@pytest.mark.contract
def test_create_video_returns_pending_video(client, token):
    response = client.create_video(token=token)

    assert response.status_code == 201, response.text
    data = response.json()
    assert data["id"]
    assert data["status"] == "pending"


@pytest.mark.known_bug
def test_video_title_is_persisted(client, token, strict_known_bugs):
    expected_title = "My Custom Video"

    response = client.create_video(title=expected_title, token=token)
    assert response.status_code == 201, response.text
    data = response.json()

    assert_known_bug(
        data.get("title") == expected_title,
        f"Expected title {expected_title!r}, got {data.get('title')!r}",
        strict_known_bugs,
    )


@pytest.mark.contract
def test_delete_video_removes_video(client, token, created_video):
    video_id = created_video["id"]

    delete_response = client.delete_video(video_id, token=token)
    assert delete_response.status_code == 204, delete_response.text

    get_response = client.get_video(video_id, token=token)
    assert get_response.status_code == 404, get_response.text


@pytest.mark.negative
@pytest.mark.known_bug
def test_delete_video_twice_returns_not_found(client, token, created_video, strict_known_bugs):
    video_id = created_video["id"]

    first = client.delete_video(video_id, token=token)
    second = client.delete_video(video_id, token=token)

    assert first.status_code == 204, first.text
    assert_known_bug(
        second.status_code == 404,
        f"Expected second delete to return 404, got {second.status_code}: {second.text}",
        strict_known_bugs,
    )
