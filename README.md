# SignSetu API QA Automation

Production-ready pytest automation for the SignSetu video caption processing API.

The project validates the full API workflow:

1. Authenticate with `X-Candidate-ID`
2. Create a video
3. Trigger caption processing
4. Verify the video can be fetched
5. Delete the video
6. Verify cleanup

It also covers negative behavior, token expiry, async workflow concerns, and cross-candidate authorization.

## Project Structure

```text
SignSetu/
├── api_client.py              # Reusable requests client with auth helpers
├── conftest.py                # Pytest fixtures, env loading, CLI options
├── pytest.ini                 # Marker and discovery configuration
├── requirements.txt
├── BUG_REPORT.md              # Product bugs represented by known-bug tests
├── scripts/
│   └── run_tests.py           # Convenience test runner
└── tests/
    ├── test_auth.py
    ├── test_video.py
    ├── test_processing.py
    ├── test_negative.py
    ├── test_security.py
    ├── test_async.py
    └── test_e2e.py
```

## Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Create local environment config:

```bash
cp .env.example .env
```

Default `.env` values:

```env
SIGNSETU_BASE_URL=https://qa-testing-navy.vercel.app
SIGNSETU_CANDIDATE_PREFIX=SignSetuQA
SIGNSETU_TIMEOUT=10
```

## Run Tests

Run the full suite:

```bash
python -m pytest -v
```

Run through the helper:

```bash
python scripts/run_tests.py
```

Run only stable contract tests:

```bash
python -m pytest -v -m "contract"
```

Skip intentionally slow tests:

```bash
python -m pytest -v -m "not slow"
```

Run known product bugs as hard failures for evidence:

```bash
python -m pytest -v --strict-known-bugs
```

Override the API target:

```bash
python -m pytest -v --base-url https://qa-testing-navy.vercel.app
```

## Test Design

- Tests use a unique candidate id per client to avoid state collisions between runs.
- The API client centralizes auth headers, timeouts, token handling, and endpoint paths.
- Known product bugs are marked with `@pytest.mark.known_bug`.
- By default, observed known bugs are reported as `xfail` instead of breaking the whole regression run.
- `--strict-known-bugs` flips those same tests into fail-fast evidence mode.

## Important Known Bugs

See [BUG_REPORT.md](BUG_REPORT.md) for details.

Top issues currently covered:

- Video title may not be persisted.
- Duplicate caption processing requests may be accepted.
- Cross-candidate video deletion may be allowed.
- Reauthentication for the same candidate may return `409 StateCollision`.
- Short token lifetime complicates long-running workflow checks.
- Repeated delete may return success even after the resource is gone.
