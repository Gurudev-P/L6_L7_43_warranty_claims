"""Hypothesis fuzz tests for the warranty-claims input functions."""

import math

import pytest
from hypothesis import given, settings, strategies as st

from warranty_claims import age_average, parse_claim, payable_charge


@settings(max_examples=200, deadline=None)
@given(st.one_of(st.none(), st.text()))
def test_parse_claim_handles_arbitrary_input(value):
    """Accept valid input or raise a documented validation exception."""
    try:
        result = parse_claim(value)
    except (TypeError, ValueError):
        return

    assert isinstance(value, str)
    assert isinstance(result, tuple) and len(result) == 2
    plan, months = result
    assert isinstance(plan, str) and plan.strip()
    assert plan == plan.strip().title()
    assert isinstance(months, float)
    assert math.isfinite(months) and months >= 0


@settings(max_examples=200, deadline=None)
@given(st.one_of(st.none(), st.text()))
def test_age_average_handles_arbitrary_input(value):
    """Return a non-negative integer average or reject malformed input."""
    try:
        result = age_average(value)
    except (TypeError, ValueError):
        return

    assert isinstance(value, str)
    assert isinstance(result, int) and not isinstance(result, bool)
    assert result >= 0
    parts = [part.strip() for part in value.split(",")]
    assert parts and all(part for part in parts)
    ages = [int(part) for part in parts]
    assert all(age >= 0 for age in ages)
    assert result == sum(ages) // len(ages)


@settings(max_examples=200, deadline=None)
@given(st.one_of(st.none(), st.text()))
def test_payable_charge_handles_arbitrary_input(value):
    """Return a finite non-negative amount or reject malformed input."""
    try:
        result = payable_charge(value)
    except (TypeError, ValueError):
        return

    assert isinstance(value, str)
    assert isinstance(result, (int, float))
    assert math.isfinite(result) and result >= 0
    parts = value.split("|")
    assert len(parts) == 2
    charge, discount = (float(part.strip()) for part in parts)
    assert charge >= 0 and discount >= 0
    assert math.isclose(result, max(charge * 1.18 - discount, 0.0))


@pytest.mark.parametrize("value", [None, 7, [], {}, True])
def test_parse_claim_rejects_non_string_input(value):
    with pytest.raises(TypeError):
        parse_claim(value)


@pytest.mark.parametrize(
    "value",
    ["", ":12", "basic:", "basic:1:2", "basic:NaN", "basic:inf", "basic:-1"],
)
def test_parse_claim_rejects_malformed_or_invalid_values(value):
    with pytest.raises(ValueError):
        parse_claim(value)


def test_parse_claim_valid_input_and_whitespace():
    assert parse_claim(" standard : 30.5 ") == ("Standard", 30.5)


@pytest.mark.parametrize("value", [None, 7, [], {}, True])
def test_age_average_rejects_non_string_input(value):
    with pytest.raises(TypeError):
        age_average(value)


@pytest.mark.parametrize("value", ["", "1,,2", ",1", "1,", "1,-2", "1,2.5"])
def test_age_average_rejects_malformed_or_invalid_values(value):
    with pytest.raises(ValueError):
        age_average(value)


def test_age_average_valid_input_and_whitespace():
    assert age_average(" 12, 24, 36 ") == 24
    assert age_average("7") == 7


@pytest.mark.parametrize("value", [None, 7, [], {}, True])
def test_payable_charge_rejects_non_string_input(value):
    with pytest.raises(TypeError):
        payable_charge(value)


@pytest.mark.parametrize(
    "value",
    ["", "100", "100|20|5", "|20", "100|", "NaN|0", "inf|0", "-10|0", "10|-2"],
)
def test_payable_charge_rejects_malformed_or_invalid_values(value):
    with pytest.raises(ValueError):
        payable_charge(value)


def test_payable_charge_valid_input_and_zero_floor():
    assert payable_charge("1500|200") == 1570
    assert payable_charge("100|500") == 0
    assert payable_charge(" 100 | 18 ") == 100
