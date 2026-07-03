Commit Story — change log

1) Initial: Project skeleton and API

   - Added a small Flask app with in-memory inventory, external lookup,
     CLI, and tests. This was the project's starting point — a working demo
     to explore inventory workflows.

2) Update README and documentation tone

   - Revise `README.md` to describe the project clearly, with setup commands,
     examples, and a reference to the commit summary.

3) Make tests read like scenarios

   - Update `test_app.py` so each test carries a short docstring describing
     the scenario it covers. This keeps the suite useful for both checks
     and readers who want to follow the expected behavior step-by-step.

4) Add CI + extra external API tests

   - Add a GitHub Actions workflow to run the test suite on push and pull requests.
   - Add `tests/test_external_success.py` which mocks successful external API
     responses and verifies the application consumes and stores returned product
     data correctly.

Notes on committing

- These additions are staged on a feature branch and committed with clear,
  descriptive messages that document the change history.
