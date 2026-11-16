"""Warranty claims: warranty coverage, claim eligibility, and SLA status."""

COVERED_MONTHS = {"basic": 12, "standard": 24, "premium": 36}


def out_of_warranty_charge(plan, age_months, claim_type, is_registered):
    """Calculate repair charge for product age beyond plan coverage."""
    if plan not in COVERED_MONTHS:
        raise ValueError("unknown plan")
    if isinstance(age_months, bool) or not isinstance(age_months, int) or age_months < 0:
        raise ValueError("invalid age")
    if claim_type not in {"accidental", "defect"}:
        raise ValueError("unknown claim type")
    if not isinstance(is_registered, bool):
        raise ValueError("registration flag must be boolean")

    covered = COVERED_MONTHS[plan]
    if is_registered and plan != "premium":
        covered += 6
    excess = age_months - covered
    if excess <= 0:
        return 0
    rate = 200 if claim_type == "accidental" else 100
    if excess > 12:
        rate += 50
        if claim_type == "accidental":
            rate += 25
    return excess * rate


def claim_allowed(days_since_last_claim, claims_filed, is_recall):
    """Return whether another claim is permitted under the policy rules."""
    if (isinstance(days_since_last_claim, bool)
            or not isinstance(days_since_last_claim, int)
            or days_since_last_claim < 0):
        raise ValueError("days since last claim must be a non-negative integer")
    if isinstance(claims_filed, bool) or not isinstance(claims_filed, int) or claims_filed < 0:
        raise ValueError("claims filed must be a non-negative integer")
    if not isinstance(is_recall, bool):
        raise ValueError("recall flag must be boolean")
    if is_recall:
        return claims_filed <= 5
    if days_since_last_claim < 30:
        return False
    return claims_filed <= 2


def sla_status(hours_left, is_hardware, is_priority):
    """Classify service-level status using hardware and priority cutoffs."""
    if (isinstance(hours_left, bool)
            or not isinstance(hours_left, (int, float))
            or hours_left < 0):
        raise ValueError("hours left must be a non-negative number")
    if not isinstance(is_hardware, bool) or not isinstance(is_priority, bool):
        raise ValueError("hardware and priority flags must be boolean")

    cutoff = 48 if is_hardware else 24
    if is_priority:
        cutoff += 24
    if hours_left >= cutoff:
        return "on_track"
    if hours_left >= cutoff - 12:
        return "at_risk"
    return "critical"
