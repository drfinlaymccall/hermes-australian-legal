"""Pure preparation gates, quote checks and an explicit scenario formula.

These helpers neither infer legal merits nor authorise another tool's actions.
"""
import datetime
import re
from decimal import Decimal, InvalidOperation, localcontext, ROUND_HALF_EVEN

DISCLAIMER = "Preparation for Australian counsel, not legal or tax advice."


def review_gate(*, confidentiality_confirmed, privilege_reviewed,
                playbook_counsel_approved):
    fields = (confidentiality_confirmed, privilege_reviewed, playbook_counsel_approved)
    if any(type(value) is not bool for value in fields):
        raise ValueError("Approval fields must be explicit JSON booleans.")
    blockers = []
    if not confidentiality_confirmed:
        blockers.append("Confirm that the NDA permits the selected AI service before supplying confidential material.")
    if not privilege_reviewed:
        blockers.append("Ask counsel about privilege and the selected AI service before supplying advice or deal documents.")
    status = "blocked" if blockers else "ready_for_counsel_playbook_review" if playbook_counsel_approved else "ungraded"
    return {"status": status, "blockers": blockers,
            "can_grade": not blockers and playbook_counsel_approved,
            "authority": "user_attested_not_independently_verified",
            "can_send_or_file": False,
            "notice": "Without a counsel-approved playbook, describe clauses but do not assign negotiation grades.",
            "disclaimer": DISCLAIMER}


def _number(value):
    # Fixed decimal strings avoid binary float surprises and exponent resource attacks.
    if isinstance(value, bool) or not isinstance(value, (str, int)):
        raise ValueError("Use a non-negative fixed decimal string or integer.")
    value = str(value)
    if not re.fullmatch(r"[0-9]{1,15}(?:\.[0-9]{1,6})?", value):
        raise ValueError("Use at most 15 integer digits and six decimal places; no exponent, comma or sign.")
    try:
        result = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError("Invalid decimal.") from exc
    return result


def earnout(*, metric, threshold, rate, cap):
    """Model one linear, capped hypothetical payout; no contractual interpretation."""
    m, t, r, c = [_number(x) for x in (metric, threshold, rate, cap)]
    with localcontext() as context:
        context.prec = 60
        payout = min(c, max(Decimal(0), m - t) * r)
        # Half-even rounding is explicit, not an assumed contract term.
        rounded = payout.quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
    return {"payout": str(rounded), "unrounded_payout": str(payout),
            "inputs": dict(metric=str(m), threshold=str(t), rate=str(r), cap=str(c)),
            "formula": "min(cap, max(0, metric - threshold) * rate)",
            "rounding": "half-even to 2 decimal places",
            "assumptions": ["All money inputs use one currency and unit.",
                            "A hypothetical linear excess-over-threshold formula, not a reading of a contract.",
                            "No tax, discounting, employment forfeiture, set-off or multi-year carry-forward."],
            "disclaimer": DISCLAIMER}


def check_finding(*, clause_text, clause_quote, source, source_quote, date):
    """Check literal inclusion only. Caller-supplied source is not authenticated."""
    for name, text in (("clause_text",clause_text),("clause_quote",clause_quote),
                       ("source_quote",source_quote),("date",date)):
        if not isinstance(text,str) or not text.strip() or len(text)>60000:
            raise ValueError(name + " must be nonempty bounded text.")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}",date):
        raise ValueError("Use YYYY-MM-DD.")
    datetime.date.fromisoformat(date)
    if not isinstance(source,dict) or source.get("date")!=date:
        raise ValueError("Source and requested dates must match.")
    if clause_quote not in clause_text or source_quote not in source.get("text",""):
        raise ValueError("A quote does not occur literally in the supplied text.")
    if not all(isinstance(source.get(k),str) and re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})",source[k])
               for k in ("corpus_commit","compilation_commit")):
        raise ValueError("Supply full corpus and compilation commit handles.")
    caveats=source.get("caveats",[])
    if not isinstance(caveats,list) or not all(isinstance(x,str) for x in caveats):
        raise ValueError("Caveats must be a list of text.")
    return {"status":"quote_match_only", "clause_quote":clause_quote,
            "source_quote":source_quote, "date":date,
            "caveats":caveats, "corpus_commit":source["corpus_commit"],
            "compilation_commit":source["compilation_commit"],
            "source_authenticity_verified":False, "legal_correctness_verified":False,
            "notice":"Literal match against supplied text only. Verify the source with au_legal_provision and the official Register.",
            "disclaimer":DISCLAIMER}
