# Lab 7 — Fuzz Testing with Hypothesis

## Objective

Use property-based fuzz testing to identify input-validation weaknesses in the warranty-claims application, then harden the three functions against unexpected and invalid input.

## Submission files

- `warranty_claims.py` — fixed application with validation for `parse_claim`, `age_average`, and `payable_charge`.
- `test_warranty_claims.py` — Hypothesis property-based tests plus deterministic edge-case tests.
- `requirements.txt` — pytest and Hypothesis dependencies.
- `Lab7_Screenshots.pdf` — four-page evidence PDF required by the lab handout. It should be stored in this `Lab 7/` directory.

## Run on macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python warranty_claims.py
python -m pytest -q test_warranty_claims.py
```

For the interactive program, use these sample inputs:

- `standard:30`
- `12,24,36`
- `1500|200`

Expected results:

```text
Plan and Age: ('Standard', 30.0)
Average Age: 24
Payable Charge: 1570.0
```

## Verification results

- Original application under Hypothesis: 27 failed, 16 passed. The tests exposed uncaught exceptions for non-string inputs and invalid values accepted by the original functions.
- Corrected application: 43 tests passed in the student's recorded run.
- The corrected application preserves the expected valid-input calculation results.

## Input validation

- Non-string input raises `TypeError`.
- Malformed separators, empty fields, negative values, non-finite numbers, malformed CSV values, and invalid numeric values raise `ValueError`.
- Valid inputs retain the starter program's calculation behavior.

## Screenshot evidence

The Lab 7 handout requires a PDF containing four evidence screenshots, in this order:

1. Original application run before fuzz testing.
2. Hypothesis failures against the original implementation.
3. Corrected application run.
4. Hypothesis tests passing against the corrected implementation.

Place the evidence file at `Lab 7/Lab7_Screenshots.pdf` before considering the repository complete for submission.
