# SignSetu API Bug Report

## Summary

The suite validates authentication, video creation, deletion, caption processing, negative cases, and cross-candidate authorization. Known product defects are represented as `@pytest.mark.known_bug` tests. By default those tests are marked `xfail` when the bug is observed; run with `--strict-known-bugs` to make them fail for evidence capture.

## Known Bugs Covered

### 1. Video title is not persisted

- **Test:** `tests/test_video.py::test_video_title_is_persisted`
- **Expected:** Created video returns the submitted title.
- **Observed:** API may return a default title such as `New Video`.
- **Impact:** User-provided metadata is discarded.

### 2. Duplicate processing requests are accepted

- **Test:** `tests/test_processing.py::test_duplicate_processing_request_is_rejected`
- **Expected:** A second processing request for an in-progress video returns `400` or `409`.
- **Observed:** API may return `202` again.
- **Impact:** Duplicate background jobs can be scheduled for the same video.

### 3. Cross-candidate delete is allowed

- **Test:** `tests/test_security.py::test_cross_candidate_delete_is_forbidden`
- **Expected:** Candidate B cannot delete Candidate A's video.
- **Observed:** API may return `204` and delete the resource.
- **Impact:** Critical authorization breach and data loss risk.

### 4. Same-candidate reauthentication fails

- **Test:** `tests/test_auth.py::test_same_candidate_can_reauthenticate`
- **Expected:** Reauth returns a fresh token.
- **Observed:** API may return `409 StateCollision`.
- **Impact:** Token refresh and repeat test execution become unreliable.

### 5. Reauthentication after async wait fails

- **Test:** `tests/test_async.py::test_can_reauthenticate_after_processing_wait`
- **Expected:** Candidate can obtain a fresh token after waiting for processing.
- **Observed:** API may return conflict instead of a new token.
- **Impact:** Long-running workflow validation is difficult with short-lived tokens.

### 6. Repeated delete returns success

- **Test:** `tests/test_video.py::test_delete_video_twice_returns_not_found`
- **Expected:** Deleting an already-deleted video returns `404`.
- **Observed:** API may return `204` again.
- **Impact:** Clients cannot distinguish a successful deletion from a resource that was already gone.

## Recommended Execution

Normal regression run:

```bash
python -m pytest -v
```

Evidence run that fails on known bugs:

```bash
python -m pytest -v --strict-known-bugs
```

Fast contract-only run:

```bash
python -m pytest -v -m "contract"
```
