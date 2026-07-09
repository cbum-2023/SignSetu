import time


def test_full_video_lifecycle(client, token):

    # Create
    create_response = client.create_video(token)

    assert create_response.status_code == 201

    video_id = create_response.json()["id"]

    # Trigger processing
    process_response = client.process_video(
        token,
        video_id
    )

    assert process_response.status_code == 202

    # Verify video exists
    get_response = client.get_video(
        token,
        video_id
    )

    assert get_response.status_code == 200

    # Delete video
    delete_response = client.delete_video(
        token,
        video_id
    )

    assert delete_response.status_code == 204

    # Verify deletion
    verify_response = client.get_video(
        token,
        video_id
    )

    assert verify_response.status_code == 404