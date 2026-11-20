"""Validate researcher-supplied quote evidence; never fetch or invent rates."""
from datetime import datetime, timedelta, timezone
from math import isfinite
from urllib.parse import urlsplit

MAX_AGE = timedelta(hours=24)
UNKNOWN_POLICY = "Not verified for this fare/room rate; confirm cancellation, change fees and deadlines at checkout."


def evidence_error(evidence, amount, context, now):
    if not isinstance(evidence, dict):
        return "missing evidence"
    if not isinstance(evidence.get("source"), str) or not evidence["source"].strip():
        return "missing source"
    try:
        url = urlsplit(evidence.get("url", ""))
        if url.scheme not in ("http", "https") or not url.hostname or url.username or url.password:
            return "source URL must be an HTTP(S) booking/search URL"
    except (ValueError, TypeError):
        return "invalid source URL"
    try:
        captured = datetime.fromisoformat(evidence["captured_at"].replace("Z", "+00:00"))
        if captured.utcoffset() is None:
            return "capture timestamp needs a timezone"
    except (KeyError, ValueError, TypeError, AttributeError):
        return "missing/invalid ISO capture timestamp"
    age = now - captured
    if age < timedelta(0):
        return "capture timestamp is in the future"
    if age > MAX_AGE:
        return "quote is older than 24 hours"
    if evidence.get("currency") != "INR":
        return "quote currency must be INR"
    value = evidence.get("amount")
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value) or value != amount:
        return "evidence amount does not match displayed total"
    if evidence.get("context") != context:
        return "quote context does not match itinerary/party/room"
    return None


def flight_context(meta, flights, option=None):
    return dict(origin=meta["origin_code"], destination=flights["out"]["to"],
                departure=meta["departure_date"], return_date=meta["return_date"],
                travellers=meta["pax"], cabin="economy", taxes="included",
                onward=option[1] if option else flights["out"],
                returning=option[2] if option else flights["ret"])


def hotel_context(meta, hotel):
    return dict(property=hotel["name"], checkin=hotel["checkin_date"],
                checkout=hotel["checkout_date"], travellers=meta["pax"],
                rooms=meta["rooms"], room=hotel["room"], meal=hotel["meal"], taxes="included")


def validate_rates(meta, trips, now=None):
    now = now or datetime.now(timezone.utc)
    errors = []
    for trip in trips:
        fl = trip["flights"]
        quotes = [("selected flights", fl["price"], fl.get("rate"), flight_context(meta, fl))]
        quotes += [(f"flight option {i+1}", o[3], o[5] if len(o) > 5 else None,
                    flight_context(meta, fl, o)) for i, o in enumerate(fl["options"])]
        quotes += [(f"hotel {key}", h["price"], h.get("rate"), hotel_context(meta, h))
                   for key, h in trip["hotels"].items()]
        for label, amount, evidence, context in quotes:
            if isinstance(amount, bool) or not isinstance(amount, (int, float)) or not isfinite(amount) or amount < 0:
                error = "price must be a finite nonnegative number"
            else:
                error = evidence_error(evidence, amount, context, now)
            if error:
                errors.append(f'{trip["title"]}: {label}: {error}')
    return errors


def policy_text(record, amount, context, now):
    policy = record.get("cancellation")
    if not isinstance(policy, dict) or not isinstance(policy.get("text"), str) or not policy["text"].strip():
        return UNKNOWN_POLICY
    if evidence_error(policy.get("evidence"), amount, context, now):
        return UNKNOWN_POLICY
    ev = policy["evidence"]
    return f'{policy["text"]} (Source: {ev["source"]}, {ev["url"]}; captured {ev["captured_at"]})'


def source_text(evidence):
    return f'{evidence["source"]} • {evidence["captured_at"]} • {evidence["url"]}'
