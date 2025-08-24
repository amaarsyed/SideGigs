import re
from datetime import time

FREE_EMAIL = {"gmail.com","yahoo.com","outlook.com","hotmail.com","proton.me","icloud.com","aol.com"}

def _domain(email): return email.split("@")[-1].lower().strip() if email and "@" in email else ""
def _valid_email(email): return bool(email and re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email))
def _digits(s): return "".join(ch for ch in (s or "") if ch.isdigit())
def _valid_phone(phone): return 10 <= len(_digits(phone)) <= 15

def _to_time(s):
    try: h,m = s.split(":"); return time(int(h), int(m))
    except Exception: return None

def _between_school_safe(start, end):
    s = _to_time(start) if start else None
    e = _to_time(end) if end else None
    if not s or not e: return True
    return time(6,0) <= s <= time(23,0) and time(6,0) <= e <= time(23,59)

def score_employer(p):
    reasons, next_steps = [], []; score = 50
    email = (p.get("email") or "").strip().lower()
    phone = (p.get("phone") or "").strip()
    company = (p.get("company") or "").strip()
    website = (p.get("website") or "").strip().lower()
    linkedin = (p.get("linkedin") or "").strip().lower()
    location = (p.get("location") or "").strip()
    pay_rate = p.get("pay_rate")
    start_time = (p.get("start_time") or "").strip()
    end_time = (p.get("end_time") or "").strip()
    email_verified = bool(p.get("email_verified"))
    phone_verified = bool(p.get("phone_verified"))
    id_verified = bool(p.get("id_verified"))
    reports_count = int(p.get("reports_count") or 0)

    if _valid_email(email):
        reasons.append("email looks valid"); score += 5
        dom = _domain(email)
        if dom and dom not in FREE_EMAIL:
            reasons.append("uses company email domain"); score += 10
            if website and dom in website: reasons.append("email domain matches website"); score += 5
        else:
            reasons.append("using a free email domain"); next_steps.append("ask for company email if available"); score -= 5
    else:
        reasons.append("email missing or invalid"); next_steps.append("ask for a valid email"); score -= 10

    if _valid_phone(phone): reasons.append("phone looks valid"); score += 5
    else: reasons.append("phone missing or invalid"); next_steps.append("ask for a working phone number"); score -= 10

    if email_verified: reasons.append("email verified"); score += 5
    if phone_verified: reasons.append("phone verified"); score += 5
    if id_verified: reasons.append("government ID verified"); score += 10

    if website: reasons.append("website provided"); score += 5
    else: next_steps.append("ask for a website or social page")
    if linkedin: reasons.append("linkedin provided"); score += 5
    else: next_steps.append("ask for a LinkedIn or public profile")
    if company: reasons.append("company name provided"); score += 3
    else: next_steps.append("ask for company or legal name")
    if location: reasons.append("location provided"); score += 3
    else: next_steps.append("ask for job location")

    try:
        pr = float(pay_rate)
        if pr >= 12: reasons.append("pay rate seems reasonable"); score += 5
        else: reasons.append("pay rate seems low"); next_steps.append("confirm pay rate"); score -= 8
    except Exception:
        next_steps.append("ask for pay rate"); score -= 3

    if not _between_school_safe(start_time, end_time):
        reasons.append("hours look late for minors"); next_steps.append("adjust start or end time"); score -= 10

    if reports_count > 0: reasons.append(f"{reports_count} prior report(s)"); score -= min(30, 10*reports_count)

    score = max(0, min(100, score))
    rating = "green" if score >= 70 else "yellow" if score >= 40 else "red"
    seen = set(); next_steps = [s for s in next_steps if not (s in seen or seen.add(s))][:5]
    return {"score": score, "rating": rating, "reasons": reasons[:8], "next_steps": next_steps,
            "disclaimer": "This is a risk screen, not a formal background check."}

def questions_for_missing(p):
    q = []
    if not _valid_email(p.get("email","")): q.append("What is your work email?")
    if not _valid_phone(p.get("phone","")): q.append("What phone number can we reach you at?")
    if not p.get("company"): q.append("What is your company or legal name?")
    if not p.get("website"): q.append("Do you have a website or social page?")
    if not p.get("linkedin"): q.append("Do you have a LinkedIn page or profile?")
    if not p.get("location"): q.append("Where will the work take place?")
    if p.get("pay_rate") in (None, "", 0): q.append("What is the hourly pay?")
    return {"questions": q[:6]}
