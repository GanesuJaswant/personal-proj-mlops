# Lab 9: Failure Injection and Chaos Testing Report

## 1. Objectives
Verify system robustness when handling anomalous, corrupted, or out-of-distribution inputs without uncaught exceptions or container crashes.

## 2. Simulated Failure Scenarios
1. **Missing Critical Features**: `horsepower` missing from payload -> Caught by Pydantic schema validation (HTTP 422).
2. **Negative Physical Dimensions**: Negative `wheelbase` or `carlength` -> Caught by validation gate.
3. **Unseen Categorical Levels**: New car brand or engine type -> Successfully handled by `OneHotEncoder(handle_unknown='ignore')`.
4. **Extreme Numerical Outliers**: Engine size > 1000ci -> Handled safely via bounding logic.

## 3. Results Summary
- Injected Anomalies: 10
- Gracefully Handled: 10 (100%)
- Unhandled Crashes: 0
- Artifacts: `artifacts/failure_simulation_report.json`, `reports/failure_report.json`
