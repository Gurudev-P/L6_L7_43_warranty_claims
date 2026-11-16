# Lab 6 — Warranty Claims: Code and Branch Coverage

## Objective

Expand the starter pytest suite for the three functions in `warranty_claims.py` and measure statement and branch coverage.

The assigned repository README asks for 90–100% coverage. This solution tests normal inputs, invalid inputs, and the decision boundaries in all three functions.

## Files

- `warranty_claims.py` — validated warranty-claims implementation.
- `test_warranty_claims.py` — 35 parametrized pytest cases.
- `requirements.txt` — pytest and coverage dependencies.
- `pytest_results.txt` — clean test run output.
- `coverage_report.txt` — clean statement and branch coverage output.

## Run on macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
python -m coverage run --branch -m pytest -q
python -m coverage report -m
```

## Verification

The package was executed in a clean working directory:

- Pytest: 35 tests passed.
- `warranty_claims.py`: 100% statement coverage and 100% branch coverage.
- Total measured coverage: 100%.

Re-run the commands in your own fork and capture your own terminal output for any instructor-required evidence.
