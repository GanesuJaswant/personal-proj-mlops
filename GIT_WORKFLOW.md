# Git Workflow & CI/CD Development Standards

## Branching Strategy
- `main`: Production-ready, validated code branch. All automated CI checks must pass before merging.
- `feature/*`: New pipeline stages, models, or feature improvements.
- `experiment/*`: Hyperparameter tuning, candidate architectural explorations.
- `bugfix/*`: Bug fixes and patch releases.

## CI/CD Pipeline Triggers
1. **Pull Requests to `main`**:
   - Triggers `lab8_ci.yml` (Linting, Unit Tests, Pipeline Validation, Endpoint Smoke Tests).
   - Triggers `lab9_failure_tests.yml` (Failure injection, edge cases, input validation).
2. **Push to `main`**:
   - Builds and tags production container image.
   - Updates deployment artifacts and manifests.
3. **Scheduled Triggers (Cron)**:
   - Triggers `lab13_monitoring.yml` (Runs data drift detection, performance monitoring, retraining assessment).

## Commit Message Conventions
- `feat:` New pipeline stage, feature transformer, or API endpoint
- `fix:` Bug fix in validation, training, or deployment logic
- `test:` Unit, integration, or failure injection tests
- `docs:` Documentation or runbook updates
- `chore:` Dependency or configuration updates
