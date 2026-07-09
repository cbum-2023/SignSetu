# SignSetu API QA Review

## Summary Verdict

I would not approve this API for production release yet. The core happy-path workflow works: authentication, video creation, caption processing, video retrieval, deletion, and post-delete verification are all covered and mostly functional. However, the test suite exposed several high-impact issues around authorization, duplicate operations, state handling, and metadata integrity.

The most critical issue is that one candidate can delete another candidate's video. I would block release until cross-candidate deletion is fixed, duplicate processing is guarded, and token reauthentication behavior is made reliable.

## Test Scope

The automated suite validates:

- Authentication with `X-Candidate-ID`
- Video creation
- Video retrieval
- Video deletion
- Caption processing trigger
- Full end-to-end video lifecycle
- Missing headers
- Invalid video ids
- Expired token behavior
- Cross-candidate authorization
- Duplicate processing requests
- Reauthentication/state collision behavior

## Test Environment

- **API base URL:** `https://qa-testing-navy.vercel.app`
- **Framework:** Python, Pytest, Requests
- **Config:** `.env` / CLI-driven base URL support
- **Command used:**

```bash
python3 -m pytest -v
```

## Latest Test Result

```text
10 passed, 6 xfailed
```

The `xfailed` tests represent confirmed product bugs. They are intentionally marked as known bugs so the regression suite can still complete while preserving evidence of the failures.

To make known bugs fail hard:

```bash
python3 -m pytest -v --strict-known-bugs
```

## Findings

### 1. Cross-candidate video deletion is allowed

- **Where:** `DELETE /api/videos/:videoId`
- **Severity:** blocker
- **Test:** `tests/test_security.py::test_cross_candidate_delete_is_forbidden`
- **What:** Candidate B can delete a video created by Candidate A.
- **Expected:** API should return `403 Forbidden` or `404 Not Found`.
- **Actual:** API returns `204 No Content` and deletes the resource.
- **Why it matters:** This is a cross-tenant authorization vulnerability. Any candidate can destroy another candidate's data if they know or guess a video id.
- **Suggested fix:** Enforce ownership checks before deletion. The delete query should include both `videoId` and the authenticated `candidateId`.

### 2. Duplicate caption processing requests are accepted

- **Where:** `POST /api/videos/:videoId/process-captions`
- **Severity:** should-fix
- **Test:** `tests/test_processing.py::test_duplicate_processing_request_is_rejected`
- **What:** The same video can receive multiple processing requests while processing is already in progress.
- **Expected:** The second request should return `400 Bad Request` or `409 Conflict`.
- **Actual:** The API returns `202 Accepted` again.
- **Why it matters:** Duplicate jobs can waste processing resources, create race conditions, and produce inconsistent final status.
- **Suggested fix:** Track processing state atomically and reject repeat requests when status is already `processing` or `completed`.

### 3. Video title is not persisted

- **Where:** `POST /api/videos`
- **Severity:** should-fix
- **Test:** `tests/test_video.py::test_video_title_is_persisted`
- **What:** Creating a video with a custom title does not preserve the submitted title.
- **Expected:** Response should include the title sent in the request body.
- **Actual:** API returns a default title such as `New Video`.
- **Why it matters:** User-provided metadata is ignored, causing data integrity and UX issues.
- **Suggested fix:** Validate and persist `title` from the request payload instead of overwriting it with a default value.

### 4. Same candidate cannot reauthenticate cleanly

- **Where:** `POST /api/auth`
- **Severity:** should-fix
- **Test:** `tests/test_auth.py::test_same_candidate_can_reauthenticate`
- **What:** Reauthenticating with the same `X-Candidate-ID` returns a conflict.
- **Expected:** API should issue a fresh valid token.
- **Actual:** API returns `409 StateCollision`.
- **Why it matters:** Tokens expire quickly, so users and automated tests need a reliable way to refresh authentication.
- **Suggested fix:** Make authentication idempotent for the same candidate or provide a documented token refresh endpoint.

### 5. Reauthentication after async wait fails

- **Where:** `POST /api/auth` after caption processing wait
- **Severity:** should-fix
- **Test:** `tests/test_async.py::test_can_reauthenticate_after_processing_wait`
- **What:** After waiting for async caption processing, the same candidate still cannot obtain a fresh token.
- **Expected:** Candidate should be able to reauthenticate and continue polling/checking workflow state.
- **Actual:** API returns `409 StateCollision`.
- **Why it matters:** Long-running async workflows become hard to monitor because the token can expire before processing completes.
- **Suggested fix:** Allow safe reauthentication or expose a refresh-token mechanism.

### 6. Repeated delete returns success

- **Where:** `DELETE /api/videos/:videoId`
- **Severity:** nit / should-fix
- **Test:** `tests/test_video.py::test_delete_video_twice_returns_not_found`
- **What:** Deleting the same video twice returns success both times.
- **Expected:** First delete should return `204`; second delete should return `404`.
- **Actual:** Second delete also returns `204`.
- **Why it matters:** Clients cannot distinguish a real deletion from a resource that was already gone.
- **Suggested fix:** Check whether the resource exists before deletion and return `404` when it does not.

## Correct Behavior Observed

- Authentication returns a token and expiry.
- Missing `X-Candidate-ID` is rejected.
- Video creation returns `201 Created`.
- Created videos start in `pending` state.
- Caption processing returns `202 Accepted`.
- Cross-candidate caption processing is blocked.
- Invalid video ids return a client error.
- Expired tokens are rejected with `401`.
- Deleted videos are no longer retrievable.
- The full happy-path lifecycle passes.

## Automation Improvements Made

The project was enhanced to be more reliable and submission-ready:

- Added a reusable API client with centralized auth headers, timeouts, and endpoint helpers.
- Added `.env.example` and configurable `SIGNSETU_BASE_URL`.
- Added pytest markers: `contract`, `negative`, `security`, `slow`, and `known_bug`.
- Added `--strict-known-bugs` mode for evidence runs.
- Fixed nested tests that pytest was not discovering.
- Added stable fixtures for authentication and video creation.
- Added `BUG_REPORT.md` for focused defect documentation.
- Added `scripts/run_tests.py` as a convenient runner.

## Final Recommendation

Request changes before release. The top three fixes I would require are:

1. Fix cross-candidate deletion authorization.
2. Prevent duplicate caption-processing jobs.
3. Support reliable reauthentication or token refresh.

After those are fixed, I would rerun the suite with:

```bash
python3 -m pytest -v --strict-known-bugs
```

The goal would be to convert the current known-bug `xfail` tests into normal passing regression tests.
