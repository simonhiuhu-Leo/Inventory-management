Commit Story — human-friendly change log

1) Initial: Project skeleton and API

   - Added a small Flask app with in-memory inventory, external lookup,
     CLI, and tests. This was the project's starting point — a working demo
     to explore inventory workflows.

2) Make docs human and story-driven

   - Turn `README.md` into a friendlier narrative that explains the project
     with quickstart commands, examples, and a pointer to this commit story.

3) Make tests read like scenes

   - Update `test_app.py` so each test carries a short docstring describing
     the scenario it covers. This keeps the suite useful for both checks
     and human readers who want to follow the expected behavior step-by-step.

4) Add CI + extra narrative tests

   - Add a GitHub Actions workflow to run the test suite on push and pull requests.
   - Add `tests/test_external_success.py` which mocks successful external API
     responses and verifies the application consumes and stores returned product
     data correctly.

Notes on committing

- These additions are staged on a feature branch and committed with humanized
  messages that read like small change-logs. If you want, I can push the branch
  to a remote and open a pull request.

Notes on committing

- These notes are written as if they were sequential commits. If you'd like,
  I can create real git commits with these messages in the repository.
