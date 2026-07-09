from __future__ import annotations

import os
from pathlib import Path

import pytest

from api_client import ApiClient, DEFAULT_BASE_URL


def _load_env_file() -> None:
    env_path = Path(__file__).with_name(".env")
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("'\""))


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--base-url",
        action="store",
        default=None,
        help="Target API base URL. Defaults to SIGNSETU_BASE_URL or the assignment API.",
    )
    parser.addoption(
        "--strict-known-bugs",
        action="store_true",
        default=False,
        help="Fail tests for known product bugs instead of marking them xfail.",
    )


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "contract: expected API behavior")
    config.addinivalue_line("markers", "negative: invalid input or expired-token behavior")
    config.addinivalue_line("markers", "security: authorization and isolation checks")
    config.addinivalue_line("markers", "known_bug: behavior currently observed as a product bug")
    config.addinivalue_line("markers", "slow: tests that intentionally wait for async/token behavior")


@pytest.fixture(scope="session", autouse=True)
def load_environment() -> None:
    _load_env_file()


@pytest.fixture(scope="session")
def base_url(pytestconfig: pytest.Config) -> str:
    return (
        pytestconfig.getoption("--base-url")
        or os.getenv("SIGNSETU_BASE_URL")
        or DEFAULT_BASE_URL
    ).rstrip("/")


@pytest.fixture(scope="session")
def strict_known_bugs(pytestconfig: pytest.Config) -> bool:
    return bool(pytestconfig.getoption("--strict-known-bugs"))


@pytest.fixture
def client(base_url: str) -> ApiClient:
    return ApiClient(base_url=base_url)


@pytest.fixture
def token(client: ApiClient) -> str:
    return client.authenticate()


@pytest.fixture
def created_video(client: ApiClient, token: str) -> dict:
    response = client.create_video(token=token)
    assert response.status_code == 201, response.text
    return response.json()


def assert_known_bug(condition: bool, message: str, strict_known_bugs: bool) -> None:
    if condition:
        return
    if strict_known_bugs:
        pytest.fail(message)
    pytest.xfail(message)
