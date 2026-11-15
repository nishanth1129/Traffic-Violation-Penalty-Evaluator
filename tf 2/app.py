"""Penalty Eval - Flask backend.

Run locally:
    pip install -r requirements.txt
    python app.py

Then open http://localhost:5000
"""

import random
from flask import Flask, render_template, jsonify, request, abort

from data.penalties import (
    VIOLATIONS,
    MODIFIERS,
    QUIZ_QUESTIONS,
    POINTS_THRESHOLDS,
    find_by_slug,
    evaluate,
    get_points_status,
    stats,
)

app = Flask(__name__)

# In-memory contact log (demo only).
CONTACT_LOG: list[dict] = []


# -------------------- HTML pages --------------------

@app.route("/")
def home():
    return render_template("index.html", page="home", stats=stats(),
                           featured=VIOLATIONS[:6])


@app.route("/evaluator")
def evaluator():
    return render_template("evaluator.html", page="evaluator",
                           violations=VIOLATIONS, modifiers=MODIFIERS)


@app.route("/violations")
def violations():
    return render_template("violations.html", page="violations",
                           violations=VIOLATIONS)


@app.route("/violations/<slug>")
def violation_detail(slug):
    v = find_by_slug(slug)
    if v is None:
        abort(404)
    related = [x for x in VIOLATIONS
               if x["category"] == v["category"] and x["slug"] != slug][:3]
    return render_template("violation.html", page="violations",
                           v=v, related=related)


@app.route("/points")
def points():
    return render_template("points.html", page="points",
                           thresholds=POINTS_THRESHOLDS)


@app.route("/guide")
def guide():
    return render_template("guide.html", page="guide")


@app.route("/about")
def about():
    return render_template("about.html", page="about")


@app.route("/contact")
def contact():
    return render_template("contact.html", page="contact")


@app.route("/stats")
def stats_page():
    return render_template("stats.html", page="stats", stats=stats(),
                           violations=VIOLATIONS)


@app.route("/quiz")
def quiz():
    return render_template("quiz.html", page="quiz",
                           questions=QUIZ_QUESTIONS)


@app.route("/resources")
def resources():
    return render_template("resources.html", page="resources")


# -------------------- JSON API --------------------

@app.route("/api/violations")
def api_violations():
    return jsonify(VIOLATIONS)


@app.route("/api/violations/<slug>")
def api_violation(slug):
    v = find_by_slug(slug)
    if v is None:
        return jsonify({"error": "not found"}), 404
    return jsonify(v)


@app.route("/api/modifiers")
def api_modifiers():
    return jsonify(MODIFIERS)


@app.route("/api/evaluate", methods=["POST"])
def api_evaluate():
    body = request.get_json(silent=True) or {}
    slug = body.get("slug")
    mods = body.get("modifiers", [])
    tier = body.get("tier_index")
    if not slug:
        return jsonify({"error": "slug required"}), 400
    try:
        result = evaluate(slug, mods, tier)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    return jsonify(result)


@app.route("/api/points/<int:points>")
def api_points(points):
    return jsonify(get_points_status(points))


@app.route("/api/quiz")
def api_quiz():
    qs = list(QUIZ_QUESTIONS)
    random.shuffle(qs)
    return jsonify(qs)


@app.route("/api/contact", methods=["POST"])
def api_contact():
    body = request.get_json(silent=True) or {}
    name = (body.get("name") or "").strip()
    email = (body.get("email") or "").strip()
    message = (body.get("message") or "").strip()
    if not name or not email or not message:
        return jsonify({"error": "all fields required"}), 400
    if "@" not in email:
        return jsonify({"error": "invalid email"}), 400
    CONTACT_LOG.append({"name": name, "email": email, "message": message})
    return jsonify({"ok": True, "message": "Thanks - we received your note."})


@app.route("/api/stats")
def api_stats():
    return jsonify(stats())


# -------------------- Errors --------------------

@app.errorhandler(404)
def not_found(_):
    return render_template("404.html", page="404"), 404


# -------------------- Template globals --------------------

@app.context_processor
def inject_globals():
    return {
        "site_name": "PenaltyEval",
        "nav_links": [
            ("Home", "/"),
            ("Evaluator", "/evaluator"),
            ("Violations", "/violations"),
            ("Points", "/points"),
            ("Guide", "/guide"),
            ("Quiz", "/quiz"),
            ("Stats", "/stats"),
            ("Resources", "/resources"),
            ("About", "/about"),
            ("Contact", "/contact"),
        ],
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
