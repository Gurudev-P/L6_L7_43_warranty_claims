"""Validated input functions for the warranty claims exercise."""

import math


def _require_text(value, field_name):
    """Ensure an input field is a string before processing it."""
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    return value


def _finite_non_negative_number(value, field_name):
    """Convert text to a finite, non-negative float."""
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must be a valid number") from exc
    if not math.isfinite(number) or number < 0:
        raise ValueError(f"{field_name} must be finite and non-negative")
    return number


def parse_claim(text):
    """Parse a claim string formatted as plan:age-in-months.

    Returns a title-cased plan name and a non-negative finite age in months.
    Raises TypeError for non-string input and ValueError for malformed values.
    """
    text = _require_text(text, "claim")
    if text.count(":") != 1:
        raise ValueError("claim must contain exactly one ':' separator")

    plan_text, months_text = text.split(":")
    plan = plan_text.strip()
    if not plan:
        raise ValueError("plan must not be empty")

    months_text = months_text.strip()
    if not months_text:
        raise ValueError("age in months must not be empty")
    months = _finite_non_negative_number(months_text, "age in months")
    return plan.title(), months


def age_average(ages_csv):
    """Return the floor average of comma-separated non-negative integer ages."""
    ages_csv = _require_text(ages_csv, "ages")
    if not ages_csv.strip():
        raise ValueError("at least one age is required")

    parts = [part.strip() for part in ages_csv.split(",")]
    if any(not part for part in parts):
        raise ValueError("age list contains an empty value")

    try:
        ages = [int(part) for part in parts]
    except ValueError as exc:
        raise ValueError("all ages must be integers") from exc

    if any(age < 0 for age in ages):
        raise ValueError("ages must be non-negative")
    return sum(ages) // len(ages)


def payable_charge(text):
    """Calculate 18% tax less discount, with a floor of zero.

    The input format is charge|discount. Both amounts must be finite and
    non-negative numbers. Raises TypeError for non-string input and ValueError
    for malformed or invalid values.
    """
    text = _require_text(text, "charge details")
    if text.count("|") != 1:
        raise ValueError("charge details must contain exactly one '|' separator")

    charge_text, discount_text = text.split("|")
    if not charge_text.strip() or not discount_text.strip():
        raise ValueError("charge and discount are both required")

    charge = _finite_non_negative_number(charge_text.strip(), "charge")
    discount = _finite_non_negative_number(discount_text.strip(), "discount")
    total = charge * 1.18 - discount
    if not math.isfinite(total):
        raise ValueError("calculated charge is outside the supported numeric range")
    return max(total, 0.0)


def main():
    """Run the three warranty-claim examples interactively."""
    print("==== Running parse_claim ====")
    user_input = input("Enter plan:age in months (e.g. standard:30): ")
    result = parse_claim(user_input)
    print("Plan and Age:", result)

    print("\n==== Running age_average ====")
    user_input = input("Enter product ages as CSV (e.g. 12,24,36): ")
    result = age_average(user_input)
    print("Average Age:", result)

    print("\n==== Running payable_charge ====")
    user_input = input("Enter charge|discount (e.g. 1500|200): ")
    result = payable_charge(user_input)
    print("Payable Charge:", result)


if __name__ == "__main__":
    main()
