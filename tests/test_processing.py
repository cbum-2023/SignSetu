def test_duplicate_processing_request(client, token):
    
    video = client.create_video(token)

    video_id = video.json()["id"]

    first = client.process_video(
        token,
        video_id
    )

    second = client.process_video(
        token,
        video_id
    )

    print("FIRST:", first.status_code)
    print("SECOND:", second.status_code)

    assert second.status_code in [400, 409]