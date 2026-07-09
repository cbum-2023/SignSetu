import pytest

from conftest import assert_known_bug


@pytest.mark.security
@pytest.mark.known_bug
def test_cross_candidate_delete_is_forbidden(client, token, strict_known_bugs):
    video = client.create_video(token=token)
    assert video.status_code == 201, video.text
    video_id = video.json()["id"]

    peer, peer_token = client.create_authenticated_peer("DeletePeer")
    delete_response = peer.delete_video(video_id, token=peer_token)

    assert_known_bug(
        delete_response.status_code in {403, 404},
        f"Expected cross-candidate delete to be forbidden, got {delete_response.status_code}: {delete_response.text}",
        strict_known_bugs,
    )


@pytest.mark.security
def test_cross_candidate_process_is_forbidden(client, token):
    video = client.create_video(token=token)
    assert video.status_code == 201, video.text
    video_id = video.json()["id"]

    peer, peer_token = client.create_authenticated_peer("ProcessPeer")
    response = peer.process_video(video_id, token=peer_token)

    assert response.status_code in {403, 404}, response.text
