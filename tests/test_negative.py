import requests

BASE_URL = "https://qa-testing-navy.vercel.app"


def test_missing_candidate_header():

    response = requests.post(
        f"{BASE_URL}/api/auth"
    )

    print(response.status_code)
    print(response.text)

    assert response.status_code in [400, 401]

import time


def test_token_expiry_behavior(client, token):

    create = client.create_video(token)

    video_id = create.json()["id"]

    time.sleep(6)

    response = client.get_video(
        token,
        video_id
    )

    print(response.status_code)
    print(response.text)

    assert response.status_code == 401


def test_invalid_video_id(client, token):

    response = client.get_video(
        token,
        "invalid-video-id"
    )

    print(response.status_code)
    print(response.text)

    assert response.status_code in [400, 404]
    
    def test_process_nonexistent_video(client, token):
    
        response = client.process_video(
            token,
            "fake-video-id"
        )

        print(response.status_code)
        print(response.text)

        assert response.status_code in [400, 404]
        
        def test_delete_video_twice(client, token):
    
                video = client.create_video(token)

                video_id = video.json()["id"]

                first = client.delete_video(
                    token,
                    video_id
                )

                second = client.delete_video(
                    token,
                    video_id
                )

                print(first.status_code)
                print(second.status_code)

                assert second.status_code == 404