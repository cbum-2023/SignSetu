import requests
import time

BASE_URL = "https://qa-testing-navy.vercel.app"


class ApiClient:

    def __init__(self):
        self.candidate_id = f"TiyaJain-{int(time.time())}"

    def auth(self):

        response = requests.post(
            f"{BASE_URL}/api/auth",
            headers={
                "X-Candidate-ID": self.candidate_id
            }
        )

        return response

    def create_video(self, token, title="QA Test Video"):
    
            headers = {
                "X-Candidate-ID": self.candidate_id,
                "Authorization": f"Bearer {token}"
            }

            payload = {
                "title": title
            }

            return requests.post(
                f"{BASE_URL}/api/videos",
                headers=headers,
                json=payload
            )

    def get_video(self, token, video_id):

        headers = {
            "X-Candidate-ID": self.candidate_id,
            "Authorization": f"Bearer {token}"
        }

        return requests.get(
            f"{BASE_URL}/api/videos/{video_id}",
            headers=headers
        )

    def process_video(self, token, video_id):

        headers = {
            "X-Candidate-ID": self.candidate_id,
            "Authorization": f"Bearer {token}"
        }

        return requests.post(
            f"{BASE_URL}/api/videos/{video_id}/process-captions",
            headers=headers
        )
    def delete_video(self, token, video_id):
    
        headers = {
            "X-Candidate-ID": self.candidate_id,
            "Authorization": f"Bearer {token}"
        }

        return requests.delete(
            f"{BASE_URL}/api/videos/{video_id}",
            headers=headers
        )