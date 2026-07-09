import pytest


@pytest.mark.contract
def test_full_video_lifecycle(client):
    token = client.authenticate()

    create_response = client.create_video(token=token)
    assert create_response.status_code == 201, create_response.text
    video_id = create_response.json()["id"]

    process_response = client.process_video(video_id, token=token)
    assert process_response.status_code == 202, process_response.text

    get_response = client.get_video(video_id, token=token)
    assert get_response.status_code == 200, get_response.text

    delete_response = client.delete_video(video_id, token=token)
    assert delete_response.status_code == 204, delete_response.text

    verify_response = client.get_video(video_id, token=token)
    assert verify_response.status_code == 404, verify_response.text
