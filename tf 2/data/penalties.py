"""Traffic violation rules engine.

Self-contained estimator. All numbers are educational midpoints based on
common US-style penalty structures. Not legal advice.
"""

from typing import Any

VIOLATIONS: list[dict[str, Any]] = [
    {
        "slug": "speeding",
        "name": "Speeding",
        "category": "Moving Violation",
        "severity": "moderate",
        "summary": "Driving above the posted speed limit.",
        "description": (
            "Speeding is the most commonly cited traffic violation. Penalties "
            "scale steeply with how far over the limit you were going and "
            "where the violation occurred."
        ),
        "fine_min": 75,
        "fine_max": 250,
        "points": 2,
        "jail_chance": 1,
        "suspend_chance": 5,
        "tiers": [
            {"label": "1-10 mph over", "fine": 75, "points": 1},
            {"label": "11-20 mph over", "fine": 150, "points": 3},
            {"label": "21-30 mph over", "fine": 250, "points": 4},
            {"label": "31+ mph over (reckless)", "fine": 500, "points": 6},
        ],
        "examples": [
            "Going 45 in a 35 zone",
            "Driving 80 in a 65 highway zone",
            "Late for work and pushing the limit",
        ],
        "tips": [
            "Cruise control on highways prevents drift.",
            "School zones often have reduced limits during specific hours.",
            "Radar detectors are illegal in some jurisdictions.",
        ],
    },
    {
        "slug": "red-light",
        "name": "Running a Red Light",
        "category": "Moving Violation",
        "severity": "serious",
        "summary": "Entering an intersection after the signal turns red.",
        "description": (
            "Running a red light is one of the leading causes of urban "
            "intersection collisions. Many cities use automated cameras."
        ),
        "fine_min": 150,
        "fine_max": 500,
        "points": 3,
        "jail_chance": 2,
        "suspend_chance": 10,
        "examples": [
            "Trying to beat a yellow light",
            "Rolling through a red on a right turn without stopping",
            "Distracted and entering on red",
        ],
        "tips": [
            "Yellow means stop if it is safe to do so.",
            "Camera-issued tickets often do not add points but still cost money.",
            "Always come to a full stop before turning right on red.",
        ],
    },
    {
        "slug": "stop-sign",
        "name": "Stop Sign Violation",
        "category": "Moving Violation",
        "severity": "moderate",
        "summary": "Failing to come to a complete stop at a stop sign.",
        "description": (
            "A 'rolling stop' (California stop) is still a citation. Officers "
            "look for full wheel-stop and a brief pause."
        ),
        "fine_min": 100,
        "fine_max": 300,
        "points": 2,
        "jail_chance": 0,
        "suspend_chance": 3,
        "examples": ["Slowing without fully stopping", "Stopping past the line"],
        "tips": [
            "Count to two at every stop sign.",
            "Stop before the painted line, not on or past it.",
        ],
    },
    {
        "slug": "illegal-turn",
        "name": "Illegal Turn",
        "category": "Moving Violation",
        "severity": "minor",
        "summary": "U-turn, left turn, or right turn where prohibited.",
        "description": "Includes turning from a wrong lane or against signage.",
        "fine_min": 50,
        "fine_max": 200,
        "points": 2,
        "jail_chance": 0,
        "suspend_chance": 2,
        "examples": ["U-turn at a 'No U-Turn' sign", "Left turn on a red arrow"],
        "tips": [
            "Watch for posted hours - some restrictions only apply at peak times.",
            "If unsure, drive past and circle back.",
        ],
    },
    {
        "slug": "distracted-driving",
        "name": "Distracted Driving / Phone Use",
        "category": "Moving Violation",
        "severity": "serious",
        "summary": "Texting, calling, or otherwise using a phone while driving.",
        "description": (
            "Most states have hands-free laws. Penalties escalate with repeat "
            "offenses and are aggravated by causing a crash."
        ),
        "fine_min": 100,
        "fine_max": 500,
        "points": 3,
        "jail_chance": 2,
        "suspend_chance": 8,
        "examples": ["Texting at a red light", "Holding a phone while driving"],
        "tips": [
            "Mount your phone before starting the engine.",
            "Use Do Not Disturb While Driving mode.",
        ],
    },
    {
        "slug": "dui",
        "name": "Driving Under the Influence (DUI/DWI)",
        "category": "Criminal Offense",
        "severity": "criminal",
        "summary": "Operating a vehicle under the influence of alcohol or drugs.",
        "description": (
            "DUI is a criminal offense with mandatory consequences in most "
            "jurisdictions. BAC of 0.08 is the standard limit (0.04 for CDL)."
        ),
        "fine_min": 500,
        "fine_max": 5000,
        "points": 6,
        "jail_chance": 70,
        "suspend_chance": 95,
        "tiers": [
            {"label": "BAC 0.08 - 0.11 (1st offense)", "fine": 1000, "points": 6},
            {"label": "BAC 0.12 - 0.14", "fine": 1500, "points": 6},
            {"label": "BAC 0.15+ (aggravated)", "fine": 2500, "points": 8},
            {"label": "2nd+ offense", "fine": 5000, "points": 10},
        ],
        "examples": ["Driving home from a bar", "Morning-after still over limit"],
        "tips": [
            "If you drink, do not drive. Use a rideshare.",
            "Even prescription meds can trigger a DUI.",
        ],
    },
    {
        "slug": "reckless",
        "name": "Reckless Driving",
        "category": "Criminal Offense",
        "severity": "severe",
        "summary": "Willful disregard for the safety of persons or property.",
        "description": "Often charged for excessive speeding, racing, or aggressive lane changes.",
        "fine_min": 250,
        "fine_max": 2500,
        "points": 5,
        "jail_chance": 25,
        "suspend_chance": 40,
        "examples": ["Street racing", "Weaving through traffic", "30+ over the limit"],
        "tips": [
            "Reckless can be added to other charges - escalates everything.",
            "Often a misdemeanor that stays on record for years.",
        ],
    },
    {
        "slug": "no-license",
        "name": "Driving Without a License",
        "category": "Administrative Violation",
        "severity": "serious",
        "summary": "Driving without a valid license in your possession.",
        "description": "Includes expired licenses and never-licensed driving.",
        "fine_min": 100,
        "fine_max": 1000,
        "points": 4,
        "jail_chance": 10,
        "suspend_chance": 20,
        "examples": ["License expired last month", "Never obtained a license"],
        "tips": [
            "Renew online before expiration.",
            "Some states allow brief grace periods.",
        ],
    },
    {
        "slug": "no-insurance",
        "name": "Driving Without Insurance",
        "category": "Administrative Violation",
        "severity": "serious",
        "summary": "Operating a vehicle without active liability insurance.",
        "description": "Mandatory in nearly every US state. Penalties include vehicle impound.",
        "fine_min": 150,
        "fine_max": 1500,
        "points": 3,
        "jail_chance": 5,
        "suspend_chance": 30,
        "examples": ["Policy lapsed", "Never insured"],
        "tips": [
            "Set auto-pay to prevent lapses.",
            "Keep proof of insurance in your glovebox.",
        ],
    },
    {
        "slug": "expired-registration",
        "name": "Expired Registration",
        "category": "Administrative Violation",
        "severity": "minor",
        "summary": "Driving with expired vehicle registration.",
        "description": "Often a fix-it ticket - can be dismissed if you renew quickly.",
        "fine_min": 50,
        "fine_max": 300,
        "points": 1,
        "jail_chance": 0,
        "suspend_chance": 2,
        "examples": ["Tags expired last month"],
        "tips": ["Set a calendar reminder 30 days before expiration."],
    },
    {
        "slug": "seatbelt",
        "name": "Seatbelt Violation",
        "category": "Equipment Violation",
        "severity": "minor",
        "summary": "Driver or passenger not wearing a seatbelt.",
        "description": "Primary enforcement in most states - officer can stop you for this alone.",
        "fine_min": 25,
        "fine_max": 200,
        "points": 1,
        "jail_chance": 0,
        "suspend_chance": 0,
        "examples": ["Quick trip without buckling up", "Passenger not belted"],
        "tips": [
            "Driver is responsible for minor passengers.",
            "Click-it-or-Ticket campaigns increase enforcement.",
        ],
    },
    {
        "slug": "broken-tail-light",
        "name": "Broken Tail Light",
        "category": "Equipment Violation",
        "severity": "minor",
        "summary": "Non-functional brake light or tail light.",
        "description": "Usually a fix-it ticket - dismissed when repaired.",
        "fine_min": 25,
        "fine_max": 150,
        "points": 0,
        "jail_chance": 0,
        "suspend_chance": 0,
        "examples": ["Bulb burned out", "Cracked lens"],
        "tips": ["Walk around your car monthly to check all lights."],
    },
    {
        "slug": "tinted-windows",
        "name": "Illegal Window Tint",
        "category": "Equipment Violation",
        "severity": "minor",
        "summary": "Window tint darker than legally allowed.",
        "description": "Each state sets a Visible Light Transmission (VLT) percentage.",
        "fine_min": 50,
        "fine_max": 300,
        "points": 0,
        "jail_chance": 0,
        "suspend_chance": 0,
        "examples": ["Aftermarket tint below state minimum VLT"],
        "tips": ["Check your state's VLT % before tinting."],
    },
    {
        "slug": "hit-and-run",
        "name": "Hit and Run",
        "category": "Criminal Offense",
        "severity": "criminal",
        "summary": "Leaving the scene of an accident without exchanging info.",
        "description": "Felony if injuries occurred. Misdemeanor for property-only damage.",
        "fine_min": 500,
        "fine_max": 10000,
        "points": 6,
        "jail_chance": 60,
        "suspend_chance": 90,
        "examples": ["Hitting a parked car and leaving", "Fleeing after a fender-bender"],
        "tips": [
            "Always stop and exchange information, even for minor damage.",
            "Even hitting a mailbox technically requires reporting.",
        ],
    },
    {
        "slug": "parking",
        "name": "Parking Violation",
        "category": "Non-Moving Violation",
        "severity": "minor",
        "summary": "Improperly parked vehicle (meter, hydrant, no-park zone).",
        "description": "Civil infraction - usually no points and no court appearance.",
        "fine_min": 25,
        "fine_max": 250,
        "points": 0,
        "jail_chance": 0,
        "suspend_chance": 0,
        "examples": ["Expired meter", "Blocking a hydrant", "Street cleaning day"],
        "tips": [
            "Read every sign - some restrictions are time-of-day specific.",
            "Pay quickly - many cities double fines after 30 days.",
        ],
    },
]

MODIFIERS: list[dict[str, Any]] = [
    {
        "id": "school-zone",
        "label": "Inside a school zone",
        "fine_mult": 2.0,
        "points_add": 2,
        "jail_add": 5,
    },
    {
        "id": "work-zone",
        "label": "Inside a work / construction zone",
        "fine_mult": 2.0,
        "points_add": 1,
        "jail_add": 3,
    },
    {
        "id": "repeat",
        "label": "Repeat offense in past 12 months",
        "fine_mult": 1.5,
        "points_add": 1,
        "jail_add": 10,
    },
    {
        "id": "accident",
        "label": "Caused an accident",
        "fine_mult": 1.5,
        "points_add": 2,
        "jail_add": 15,
    },
    {
        "id": "minor-passenger",
        "label": "Minor passenger in vehicle",
        "fine_mult": 1.25,
        "points_add": 1,
        "jail_add": 5,
    },
    {
        "id": "commercial",
        "label": "Driving a commercial vehicle (CDL)",
        "fine_mult": 1.5,
        "points_add": 1,
        "jail_add": 5,
    },
]

POINTS_THRESHOLDS = [
    {"max": 3, "label": "Clean Record", "tone": "ok",
     "message": "No active violations of concern."},
    {"max": 7, "label": "Caution", "tone": "watch",
     "message": "On the radar - drive carefully."},
    {"max": 11, "label": "Warning Zone", "tone": "warn",
     "message": "Insurance rates likely to rise."},
    {"max": 15, "label": "Suspension Risk", "tone": "danger",
     "message": "License suspension review triggered."},
    {"max": 999, "label": "Suspended", "tone": "critical",
     "message": "License will be suspended in most states."},
]

QUIZ_QUESTIONS = [
    {
        "id": 1,
        "question": "What is the standard BAC limit for non-commercial drivers?",
        "options": ["0.05", "0.08", "0.10", "0.12"],
        "answer": 1,
        "explain": "0.08 is the legal limit in all 50 US states (0.04 for commercial drivers).",
    },
    {
        "id": 2,
        "question": "How long do most points stay on your record?",
        "options": ["6 months", "1 year", "2-3 years", "10 years"],
        "answer": 2,
        "explain": "Most states use a 2-3 year rolling window for active points.",
    },
    {
        "id": 3,
        "question": "What does running a red light typically cost in fines?",
        "options": ["$25 - $75", "$150 - $500", "$1000+", "Never just a fine"],
        "answer": 1,
        "explain": "Red light fines typically range from $150 to $500.",
    },
    {
        "id": 4,
        "question": "Which violation is usually a 'fix-it' ticket?",
        "options": ["DUI", "Reckless driving", "Broken tail light", "Hit and run"],
        "answer": 2,
        "explain": "Equipment violations like broken lights are often dismissed when repaired.",
    },
    {
        "id": 5,
        "question": "School zones typically multiply fines by:",
        "options": ["1x (no change)", "1.5x", "2x", "3x"],
        "answer": 2,
        "explain": "School zone violations commonly carry double fines.",
    },
    {
        "id": 6,
        "question": "Hit and run with injuries is usually classified as a:",
        "options": ["Civil infraction", "Misdemeanor", "Felony", "Warning only"],
        "answer": 2,
        "explain": "Hit and run involving injuries is a felony in most jurisdictions.",
    },
    {
        "id": 7,
        "question": "Which is most likely to result in license suspension?",
        "options": ["Speeding 5 mph over", "Expired tags", "Accumulating 12+ points", "Parking ticket"],
        "answer": 2,
        "explain": "Reaching the points threshold (typically 12) triggers automatic suspension review.",
    },
    {
        "id": 8,
        "question": "Defensive driving courses can typically reduce points by:",
        "options": ["0 points", "1-3 points", "All points", "Cancels insurance increase only"],
        "answer": 1,
        "explain": "Most states allow a one-time reduction of 1-3 points after a course.",
    },
]


SEVERITY_ORDER = {"minor": 0, "moderate": 1, "serious": 2, "severe": 3, "criminal": 4}


def find_by_slug(slug: str) -> dict[str, Any] | None:
    for v in VIOLATIONS:
        if v["slug"] == slug:
            return v
    return None


def evaluate(slug: str, modifier_ids: list[str], tier_index: int | None = None) -> dict[str, Any]:
    v = find_by_slug(slug)
    if v is None:
        raise ValueError(f"Unknown violation: {slug}")

    base_fine_min = float(v["fine_min"])
    base_fine_max = float(v["fine_max"])
    base_points = int(v["points"])
    base_jail = float(v["jail_chance"])
    base_suspend = float(v["suspend_chance"])

    if v.get("tiers") and tier_index is not None and 0 <= tier_index < len(v["tiers"]):
        t = v["tiers"][tier_index]
        base_fine_min = t["fine"] * 0.7
        base_fine_max = t["fine"] * 1.3
        base_points = t["points"]

    fine_mult = 1.0
    points_add = 0
    jail_add = 0.0
    applied = []

    for mid in modifier_ids:
        mod = next((m for m in MODIFIERS if m["id"] == mid), None)
        if mod is None:
            continue
        fine_mult *= mod["fine_mult"]
        points_add += mod["points_add"]
        jail_add += mod["jail_add"]
        applied.append(mod)

    fine_min = round(base_fine_min * fine_mult)
    fine_max = round(base_fine_max * fine_mult)
    points = base_points + points_add
    jail_chance = min(95, base_jail + jail_add)
    suspend_chance = min(98, base_suspend + jail_add * 0.6)

    if points >= 12:
        severity_score = 4
    elif points >= 8:
        severity_score = 3
    elif points >= 5:
        severity_score = 2
    elif points >= 2:
        severity_score = 1
    else:
        severity_score = 0

    severity_score = max(severity_score, SEVERITY_ORDER.get(v["severity"], 0))
    severity_label = ["Minor", "Moderate", "Serious", "Severe", "Criminal"][severity_score]

    insurance_pct = min(95, 5 + points * 4 + (15 if jail_chance > 30 else 0))

    summary = build_summary(v, points, jail_chance, suspend_chance)

    return {
        "violation": {
            "slug": v["slug"],
            "name": v["name"],
            "category": v["category"],
        },
        "fine_min": fine_min,
        "fine_max": fine_max,
        "points": points,
        "jail_chance": round(jail_chance),
        "suspend_chance": round(suspend_chance),
        "insurance_pct": insurance_pct,
        "severity": severity_label.lower(),
        "severity_label": severity_label,
        "modifiers_applied": [{"id": m["id"], "label": m["label"]} for m in applied],
        "summary": summary,
    }


def build_summary(v: dict[str, Any], points: int, jail_chance: float, suspend_chance: float) -> str:
    parts = [f"You are looking at {points} demerit point{'s' if points != 1 else ''}"]
    if suspend_chance > 50:
        parts.append("with a high probability of license suspension")
    elif suspend_chance > 15:
        parts.append("and a meaningful suspension risk")
    if jail_chance > 30:
        parts.append("plus possible jail time")
    elif jail_chance > 5:
        parts.append("with a small chance of jail")
    return ", ".join(parts) + "."


def get_points_status(points: int) -> dict[str, Any]:
    for tier in POINTS_THRESHOLDS:
        if points <= tier["max"]:
            return {**tier, "points": points}
    return {**POINTS_THRESHOLDS[-1], "points": points}


def stats() -> dict[str, Any]:
    severities: dict[str, int] = {}
    categories: dict[str, int] = {}
    total_fine = 0
    for v in VIOLATIONS:
        severities[v["severity"]] = severities.get(v["severity"], 0) + 1
        categories[v["category"]] = categories.get(v["category"], 0) + 1
        total_fine += (v["fine_min"] + v["fine_max"]) / 2
    return {
        "violations_count": len(VIOLATIONS),
        "modifiers_count": len(MODIFIERS),
        "avg_fine": round(total_fine / len(VIOLATIONS)),
        "max_fine": max(v["fine_max"] for v in VIOLATIONS),
        "max_points": max(v["points"] for v in VIOLATIONS),
        "by_severity": severities,
        "by_category": categories,
    }
