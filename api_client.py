"""Reusable API client for the SignSetu QA assignment.

The target API issues very short-lived tokens, so the client can authenticate,
refresh on demand, and keep request construction consistent across tests.
"""

from __future__ import annotations

import os
import time
import uuid
from dataclasses import dataclass
from typing import Any

import requests


DEFAULT_BASE_URL = "https://qa-testing-navy.vercel.app"
DEFAULT_TIMEOUT = 10


@dataclass(frozen=True)
class AuthToken:
    value: str
    expires_at: str | None = None
    issued_at: float = time.time()


class ApiClient:
    def __init__(
        self,
        base_url: str | None = None,
        candidate_id: str | None = None,
        timeout: float | None = None,
        session: requests.Session | None = None,
    ) -> None:
        self.base_url = (base_url or os.getenv("SIGNSETU_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
        self.candidate_id = candidate_id or self._candidate_id()
        self.timeout = float(timeout or os.getenv("SIGNSETU_TIMEOUT", DEFAULT_TIMEOUT))
        self.session = session or requests.Session()
        self._token: AuthToken | None = None

    @staticmethod
    def _candidate_id(prefix: str | None = None) -> str:
        safe_prefix = prefix or os.getenv("SIGNSETU_CANDIDATE_PREFIX") or "SignSetuQA"
        return f"{safe_prefix}-{int(time.time())}-{uuid.uuid4().hex[:8]}"

    def auth(self, candidate_id: str | None = None) -> requests.Response:
        return self.session.post(
            f"{self.base_url}/api/auth",
            headers={"X-Candidate-ID": candidate_id or self.candidate_id},
            timeout=self.timeout,
        )

    def authenticate(self, force: bool = False) -> str:
        if self._token and not force:
            return self._token.value

        response = self.auth()
        response.raise_for_status()
        data = response.json()
        self._token = AuthToken(value=data["token"], expires_at=data.get("expiresAt"))
        return self._token.value

    def auth_headers(self, token: str | None = None, candidate_id: str | None = None) -> dict[str, str]:
        return {
            "X-Candidate-ID": candidate_id or self.candidate_id,
            "Authorization": f"Bearer {token or self.authenticate()}",
        }

    def request(
        self,
        method: str,
        path: str,
        *,
        token: str | None = None,
        candidate_id: str | None = None,
        retry_on_expired_token: bool = True,
        **kwargs: Any,
    ) -> requests.Response:
        headers = kwargs.pop("headers", {})
        request_headers = {**self.auth_headers(token, candidate_id), **headers}
        response = self.session.request(
            method,
            f"{self.base_url}{path}",
            headers=request_headers,
            timeout=self.timeout,
            **kwargs,
        )

        if response.status_code == 401 and token is None and retry_on_expired_token:
            request_headers = {**self.auth_headers(self.authenticate(force=True), candidate_id), **headers}
            response = self.session.request(
                method,
                f"{self.base_url}{path}",
                headers=request_headers,
                timeout=self.timeout,
                **kwargs,
            )

        return response

    def create_video(self, title: str = "QA Test Video", token: str | None = None) -> requests.Response:
        return self.request("POST", "/api/videos", token=token, json={"title": title})

    def get_video(self, video_id: str, token: str | None = None) -> requests.Response:
        return self.request("GET", f"/api/videos/{video_id}", token=token)

    def process_video(self, video_id: str, token: str | None = None) -> requests.Response:
        return self.request("POST", f"/api/videos/{video_id}/process-captions", token=token)

    def delete_video(self, video_id: str, token: str | None = None) -> requests.Response:
        return self.request("DELETE", f"/api/videos/{video_id}", token=token)

    def create_authenticated_peer(self, prefix: str = "Peer") -> tuple["ApiClient", str]:
        peer = ApiClient(
            base_url=self.base_url,
            candidate_id=self._candidate_id(prefix),
            timeout=self.timeout,
        )
        return peer, peer.authenticate()
