"""Branch-complete tests for the warranty-claims functions."""

import pytest

from warranty_claims import (
    claim_allowed,
    out_of_warranty_charge,
    sla_status,
)


@pytest.mark.parametrize(
    ("plan", "age", "claim_type", "registered", "expected"),
    [
        ("basic", 12, "defect", False, 0),
        ("basic", 18, "defect", True, 0),  # registration extension boundary
        ("basic", 19, "defect", False, 700),
        ("standard", 25, "accidental", False, 200),
        ("standard", 37, "accidental", False, 275 * 13),
        ("basic", 25, "defect", False, 150 * 13),
        ("premium", 48, "defect", True, 1200),
    ],
)
def test_out_of_warranty_charge_valid_cases(plan, age, claim_type, registered, expected):
    assert out_of_warranty_charge(plan, age, claim_type, registered) == expected


@pytest.mark.parametrize(
    ("args", "message"),
    [
        (("gold", 10, "defect", False), "unknown plan"),
        (("basic", -1, "defect", False), "invalid age"),
        (("basic", 1.5, "defect", False), "invalid age"),
        (("basic", 10, "unknown", False), "unknown claim type"),
        (("basic", 10, "defect", 1), "registration flag must be boolean"),
    ],
)
def test_out_of_warranty_charge_invalid_inputs(args, message):
    with pytest.raises(ValueError, match=message):
        out_of_warranty_charge(*args)


@pytest.mark.parametrize(
    ("days", "claims", "recall", "expected"),
    [
        (0, 0, True, True),
        (0, 5, True, True),
        (0, 6, True, False),
        (29, 0, False, False),
        (30, 2, False, True),
        (60, 3, False, False),
    ],
)
def test_claim_allowed_branches(days, claims, recall, expected):
    assert claim_allowed(days, claims, recall) is expected


@pytest.mark.parametrize(
    "args",
    [
        ((-1, 0, False),),
        ((1.5, 0, False),),
        ((30, -1, False),),
        ((30, 1, 0),),
    ],
)
def test_claim_allowed_rejects_invalid_inputs(args):
    with pytest.raises(ValueError):
        claim_allowed(*args[0])


@pytest.mark.parametrize(
    ("hours", "hardware", "priority", "expected"),
    [
        (48, True, False, "on_track"),
        (36, True, False, "at_risk"),
        (35.9, True, False, "critical"),
        (24, False, False, "on_track"),
        (12, False, False, "at_risk"),
        (11.9, False, False, "critical"),
        (72, True, True, "on_track"),
        (60, True, True, "at_risk"),
        (59, True, True, "critical"),
        (48, False, True, "on_track"),
    ],
)
def test_sla_status_all_categories(hours, hardware, priority, expected):
    assert sla_status(hours, hardware, priority) == expected


@pytest.mark.parametrize(
    "args",
    [
        ((-0.1, True, False),),
        ((True, True, False),),
        ((1, 1, False),),
    ],
)
def test_sla_status_invalid_inputs(args):
    with pytest.raises(ValueError):
        sla_status(*args[0])
