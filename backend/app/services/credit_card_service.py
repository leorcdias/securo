import calendar
from datetime import date
from decimal import Decimal
from typing import Optional


def _clamp_day(year: int, month: int, day: int) -> date:
    last_day = calendar.monthrange(year, month)[1]
    return date(year, month, min(day, last_day))


def _next_day_occurrence(target_day: int, reference: date) -> date:
    candidate = _clamp_day(reference.year, reference.month, target_day)
    if candidate >= reference:
        return candidate
    if reference.month == 12:
        return _clamp_day(reference.year + 1, 1, target_day)
    return _clamp_day(reference.year, reference.month + 1, target_day)


def get_cycle_dates(
    statement_close_day: Optional[int],
    payment_due_day: Optional[int],
    reference: Optional[date] = None,
) -> dict:
    """Return the close + due dates of the nearest upcoming billing cycle.

    Both dates are from the SAME cycle: the due is anchored on the nearest upcoming
    occurrence of payment_due_day, and the close is the most recent occurrence of
    statement_close_day on or before that due date. This guarantees close <= due."""
    if reference is None:
        reference = date.today()

    next_due = _next_day_occurrence(payment_due_day, reference) if payment_due_day else None

    next_close: Optional[date] = None
    if statement_close_day:
        if next_due:
            # Pick the close that belongs to next_due's cycle: try same month first;
            # if it lands after the due date, walk back one month (with end-of-month clamping).
            anchor = next_due
            candidate = _clamp_day(anchor.year, anchor.month, statement_close_day)
            if candidate > anchor:
                if anchor.month == 1:
                    candidate = _clamp_day(anchor.year - 1, 12, statement_close_day)
                else:
                    candidate = _clamp_day(anchor.year, anchor.month - 1, statement_close_day)
            next_close = candidate
        else:
            next_close = _next_day_occurrence(statement_close_day, reference)

    return {
        "next_close_date": next_close,
        "next_due_date": next_due,
    }


def compute_available_credit(
    credit_limit: Optional[Decimal],
    current_balance: Decimal,
) -> Optional[Decimal]:
    """available = limit − utilized. current_balance for a credit card is negative when debt."""
    if credit_limit is None:
        return None
    utilized = -current_balance if current_balance < 0 else Decimal("0")
    return credit_limit - utilized
