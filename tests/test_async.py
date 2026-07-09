import requests
import time

BASE_URL = "https://qa-testing-navy.vercel.app"


def test_processing_eventually_completes():

    candidate = f"Tiya-{int(time.time())}"

    auth = requests.post(
        f"{BASE_URL}/api/auth",
        headers={"X-Candidate-ID": candidate}
    )

    token = auth.json()["token"]

    headers = {
        "X-Candidate-ID": candidate,
        "Authorization": f"Bearer {token}"
    }

    video = requests.post(
        f"{BASE_URL}/api/videos",
        headers=headers
    )

    video_id = video.json()["id"]

    requests.post(
        f"{BASE_URL}/api/videos/{video_id}/process-captions",
        headers=headers
    )

    time.sleep(8)

    auth2 = requests.post(
        f"{BASE_URL}/api/auth",
        headers={"X-Candidate-ID": candidate}
    )

    print(auth2.status_code)
    print(auth2.text)