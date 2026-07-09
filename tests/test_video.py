def test_create_video(client, token):
    
    response = client.create_video(token)

    assert response.status_code == 201

    data = response.json()

    assert "id" in data
    assert "status" in data

    assert data["status"] == "pending"


def test_video_title_persistence(client, token):

    expected_title = "My Custom Video"

    response = client.create_video(
        token,
        title=expected_title
    )

    data = response.json()

    assert data["title"] == expected_title


def test_delete_video(client, token):

    video = client.create_video(token)

    video_id = video.json()["id"]

    delete_response = client.delete_video(
        token,
        video_id
    )

    print(delete_response.status_code)
    print(delete_response.text)

    get_response = client.get_video(
        token,
        video_id
    )

    print(get_response.status_code)
    print(get_response.text)

    assert get_response.status_code == 404