import time

import pytest

from conftest import assert_known_bug


@pytest.mark.slow
@pytest.mark.known_bug
def test_can_reauthenticate_after_processing_wait(client, token, created_video, strict_known_bugs):
    response = client.process_video(created_video["id"], token=token)
    assert response.status_code == 202, response.text

    time.sleep(8)

    auth2 = client.auth()
    assert_known_bug(
        auth2.status_code == 201,
        f"Expected fresh token after wait, got {auth2.status_code}: {auth2.text}",
        strict_known_bugs,
    )
