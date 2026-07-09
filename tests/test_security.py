import requests
import time

BASE_URL = "https://qa-testing-navy.vercel.app"


def test_cross_candidate_delete_forbidden():

    candidate_a = f"A-{int(time.time())}"

    auth_a = requests.post(
        f"{BASE_URL}/api/auth",
        headers={"X-Candidate-ID": candidate_a}
    )

    token_a = auth_a.json()["token"]

    headers_a = {
        "X-Candidate-ID": candidate_a,
        "Authorization": f"Bearer {token_a}"
    }

    video = requests.post(
        f"{BASE_URL}/api/videos",
        headers=headers_a
    )

    video_id = video.json()["id"]

    candidate_b = f"B-{int(time.time())}"

    auth_b = requests.post(
        f"{BASE_URL}/api/auth",
        headers={"X-Candidate-ID": candidate_b}
    )

    token_b = auth_b.json()["token"]

    headers_b = {
        "X-Candidate-ID": candidate_b,
        "Authorization": f"Bearer {token_b}"
    }

    delete_response = requests.delete(
        f"{BASE_URL}/api/videos/{video_id}",
        headers=headers_b
    )

    print(delete_response.status_code)
    print(delete_response.text)

    assert delete_response.status_code in [403, 404]
    
    def test_duplicate_auth_same_candidate():
    
        candidate = f"Tiya-{int(time.time())}"

        first = requests.post(
            f"{BASE_URL}/api/auth",
            headers={"X-Candidate-ID": candidate}
        )

        second = requests.post(
            f"{BASE_URL}/api/auth",
            headers={"X-Candidate-ID": candidate}
        )

        print(first.status_code)
        print(second.status_code)
        print(second.text)

        assert second.status_code == 201
def test_cross_candidate_process_forbidden():
    
    candidate_a = f"A-{int(time.time())}"

    auth_a = requests.post(
        f"{BASE_URL}/api/auth",
        headers={"X-Candidate-ID": candidate_a}
    )

    token_a = auth_a.json()["token"]

    headers_a = {
        "X-Candidate-ID": candidate_a,
        "Authorization": f"Bearer {token_a}"
    }

    video = requests.post(
        f"{BASE_URL}/api/videos",
        headers=headers_a
    )

    video_id = video.json()["id"]

    candidate_b = f"B-{int(time.time())}"

    auth_b = requests.post(
        f"{BASE_URL}/api/auth",
        headers={"X-Candidate-ID": candidate_b}
    )

    token_b = auth_b.json()["token"]

    headers_b = {
        "X-Candidate-ID": candidate_b,
        "Authorization": f"Bearer {token_b}"
    }

    response = requests.post(
        f"{BASE_URL}/api/videos/{video_id}/process-captions",
        headers=headers_b
    )

    print(response.status_code)
    print(response.text)

    assert response.status_code in [403, 404]
    
def test_same_candidate_can_reauthenticate():
    
    candidate = f"Tiya-{int(time.time())}"

    first = requests.post(
        f"{BASE_URL}/api/auth",
        headers={"X-Candidate-ID": candidate}
    )

    second = requests.post(
        f"{BASE_URL}/api/auth",
        headers={"X-Candidate-ID": candidate}
    )

    print(first.status_code)
    print(second.status_code)
    print(second.text)

    assert second.status_code == 201