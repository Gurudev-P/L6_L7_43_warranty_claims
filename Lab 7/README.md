# Lab 7 - Fuzz Testing with Hypothesis

## Objective
Use property-based fuzz testing to identify input-validation weaknesses in the warranty-claims application, then harden the three functions against unexpected and invalid input.

## Files
- `warranty_claims.py` - fixed application with validation for `parse_claim`, `age_average`, and `payable_charge`.
- `test_warranty_claims.py` - Hypothesis property-based tests plus deterministic edge-case tests.
- `requirements.txt` - pytest and Hypothesis dependencies.
- `Lab7_Screenshots.pdf` - four-page screenshot evidence PDF (included in the submission ZIP).

## Run on macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python warranty_claims.py
python -m pytest -q test_warranty_claims.py
```

For the interactive program, enter `standard:30`, `12,24,36`, and `1500|200`.

Expected results:

```text
Plan and Age: ('Standard', 30.0)
Average Age: 24
Payable Charge: 1570.0
```

## Results
- Original application under Hypothesis: 27 failed, 16 passed. The tests exposed uncaught exceptions for non-string inputs and invalid values accepted by the original functions.
- Corrected application on the student's Mac: 43 tests passed.
- The corrected application preserves the valid-input calculation results.

## Input validation
- Non-string input raises `TypeError`.
- Malformed separators, empty fields, negative values, non-finite numbers, malformed CSV values, and invalid numeric values raise `ValueError`.
- Valid inputs retain the starter program's calculation behavior.

## Evidence
The handout's four screenshot requirements are addressed in `Lab7_Screenshots.pdf`, supplied in the downloadable Lab 7 submission ZIP.
