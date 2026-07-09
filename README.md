# SignSetu QA Analyst Intern Assignment

## Overview

For this assignment, I created an automated API test suite using Python, Pytest, and Requests to test the Video Caption Processing Pipeline.

My goal was not only to verify the expected workflow but also to actively identify edge cases, vulnerabilities, and data integrity issues as mentioned in the assignment.

---

## Testing Approach

I started by manually exploring the API to understand how authentication, video creation, caption processing, and deletion worked.

After understanding the workflow, I built a reusable automation framework consisting of:

* `api_client.py` for reusable API methods
* `conftest.py` for shared fixtures and setup
* Separate test files for different categories of testing

The test suite covers:

* Authentication
* Video creation
* Video deletion
* Caption processing
* End-to-end workflow testing
* Negative testing
* Security and authorization testing

---

## Handling Asynchronous Processing

One challenge I encountered was that the caption processing endpoint is asynchronous and returns `202 Accepted`.

Another challenge was that authentication tokens expire after approximately 5 seconds.

While testing, I had to account for token expiration, state-related issues, and workflow interruptions when validating longer-running operations.

---

## Project Structure

```text
signsetu/
│
├── tests/
│   ├── test_auth.py
│   ├── test_video.py
│   ├── test_processing.py
│   ├── test_negative.py
│   ├── test_security.py
│   └── test_e2e.py
│
├── api_client.py
├── conftest.py
├── requirements.txt
└── README.md
```

---

## End-to-End Workflow Covered

The automation validates the following workflow:

1. Authenticate
2. Create a video
3. Trigger caption processing
4. Verify the video exists
5. Delete the video
6. Verify cleanup

---

# Bugs Found

## Bug 1: Video Title Is Not Persisted

### Steps

1. Create a video with a custom title.
2. Check the API response.

### Expected

The response should contain the title provided in the request.

### Actual

The API always returns:

```json
{
  "title": "New Video"
}
```

### Impact

User-provided metadata is ignored, resulting in a data integrity issue.

---

## Bug 2: Duplicate Processing Requests Are Allowed

### Steps

1. Create a video.
2. Trigger caption processing.
3. Trigger caption processing again immediately.

### Expected

The second request should be rejected because processing is already in progress.

### Actual

Both requests return:

```http
202 Accepted
```

### Impact

Multiple processing jobs can be initiated for the same video.

---

## Bug 3: Cross-Candidate Video Deletion

### Steps

1. Candidate A creates a video.
2. Candidate B attempts to delete Candidate A's video.

### Expected

The request should be rejected.

### Actual

The API returns:

```http
204 No Content
```

and successfully deletes the video.

### Impact

A user can delete resources belonging to another user.

This is the most critical issue discovered during testing.

---

## Bug 4: StateCollision on Re-Authentication

### Steps

1. Authenticate using a candidate ID.
2. Attempt to authenticate again using the same candidate ID.

### Expected

A new valid token should be issued.

### Actual

The API returns:

```http
409 Conflict
```

with:

```json
{
  "error": "StateCollision"
}
```

### Impact

The same user cannot obtain a fresh token, affecting repeatability and automation reliability.

---

## Bug 5: Token Expiry Breaks Long-Running Workflow Validation

### Observation

During end-to-end execution, tokens expired before the complete lifecycle could be validated.

After deleting a video, the verification step returned:

```http
401 Unauthorized
```

instead of the expected resource state.

### Impact

Long-running workflows become difficult to monitor and validate without implementing token refresh logic.

---

## Additional Findings

### Correct Behavior Observed

* Missing `X-Candidate-ID` returns `400 Bad Request`
* Invalid video IDs return `404 Not Found`
* Deleted videos are no longer accessible
* Cross-candidate processing requests are blocked

---

## Running the Tests

Install dependencies:

```bash
pip install -r requirements.txt
```

Run all tests:

```bash
pytest -v
```

Run a specific test file:

```bash
pytest tests/test_video.py -v
```

---

## Final Notes

Some tests intentionally fail because they are designed to expose confirmed defects in the API. These failures are expected and serve as evidence of the issues discovered during testing.

Overall, this assignment helped me explore API testing, asynchronous workflows, authorization checks, and negative testing in a structured and practical way.
# SignSetu
