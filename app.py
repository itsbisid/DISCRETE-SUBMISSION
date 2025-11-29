

# 3333333
import os
import re
import json
import random
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from datetime import datetime

from logic.evaluator import (
    generate_truth_table,
    classify_formula,
    check_equivalence,
    check_argument_validity,
    normalize_formula
)
from logic.parser import parse_expression

from logic.questions import (
    check_answer,
    get_hint,
    get_random_questions
)

app = Flask(__name__)
app.secret_key = os.environ.get("LOGIC_TUTOR_SECRET", "dev-secret-key")

# Optional: load for tools/demo; quiz uses get_random_questions()
with open("questions_full_200.json", "r", encoding="utf-8") as f:
    ALL_QUESTIONS = json.load(f)


# -------------------------------------------------
# PERFORMANCE TRACKING
# -------------------------------------------------
def init_performance():
    """Ensure session has performance tracking."""
    if "performance" not in session:
        session["performance"] = {}


def update_performance(topic, correct):
    """Update attempts + correct answers for a topic."""
    perf = session.get("performance", {})

    if topic not in perf:
        perf[topic] = {"attempts": 0, "correct": 0}

    perf[topic]["attempts"] += 1
    if correct:
        perf[topic]["correct"] += 1

    session["performance"] = perf


# -------------------------------------------------
# ADAPTIVE DIFFICULTY ENGINE
# -------------------------------------------------
def get_adaptive_difficulty(topic):
    perf = session.get("performance", {})

    if topic not in perf:
        return "Easy"  # New topic → start easy

    data = perf[topic]
    attempts = data["attempts"]
    correct = data["correct"]

    if attempts == 0:
        return "Easy"

    accuracy = correct / attempts

    if accuracy < 0.40:
        return "Easy"
    elif accuracy < 0.75:
        return "Medium"
    else:
        return "Hard"


# -------------------------
# Helpers
# -------------------------
def _clean_label_prefix(text: str) -> str:
    """Remove a leading difficulty label like: [Easy] Question ..."""
    return re.sub(r"^\[[^\]]+\]\s*", "", text or "")


# -------------------------
# ROUTES: Basic pages
# -------------------------
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/learn")
def learn():
    return render_template("learn.html")

@app.route("/tools", methods=["GET", "POST"])
def tools():
    result = {}

    if request.method == "POST":
        action = request.form.get("action")

        # ------------------------------
        # 1. TRUTH TABLE
        # ------------------------------
        if action == "truth_table":
            formula = request.form.get("formula_tt", "").strip()
            formula = normalize_formula(formula)

            data = generate_truth_table(formula)

            result["headers"] = data.get("headers", [])
            result["table"] = data.get("rows", [])
            result["error"] = data.get("error")

        # ------------------------------
        # 2. FORMULA CLASSIFIER
        # ------------------------------
        elif action == "classify":
            formula = request.form.get("formula_class", "").strip()
            # Use normalized formula for classification to keep behavior consistent
            result["classification"] = classify_formula(normalize_formula(formula))

        # ------------------------------
        # 3. EQUIVALENCE CHECKER
        # ------------------------------
        elif action == "equivalence":
            f1 = normalize_formula(request.form.get("formula1", "").strip())
            f2 = normalize_formula(request.form.get("formula2", "").strip())

            result["equivalent"] = check_equivalence(f1, f2)

        # ------------------------------
        # 4. ARGUMENT VALIDITY CHECKER
        # ------------------------------
        elif action == "validity":
            premises_raw = request.form.get("premises", "")
            conclusion = normalize_formula(request.form.get("conclusion", "").strip())
            premises_list = [normalize_formula(p.strip()) for p in premises_raw.split(",") if p.strip()]

            # Validate each formula before calling the evaluator so we can show
            # a clear error message instead of a generic "Invalid formula".
            try:
                for p in premises_list:
                    parse_expression(p)
                if conclusion:
                    parse_expression(conclusion)
            except Exception as e:
                result["validity"] = f"Error: Invalid formula — {str(e)}"
            else:
                result["validity"] = check_argument_validity(premises_list, conclusion)

    return render_template("tools.html", result=result)



@app.route("/performance")
def performance():
    init_performance()
    return render_template("performance.html",
                           performance=session["performance"])


# -------------------------
# QUIZ SESSION ROUTES
# -------------------------
@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if not session.get("quiz_started"):
        return render_template("quiz.html", question=None)

    index = session.get("quiz_index", 0)
    questions = session.get("quiz_questions", [])

    if index >= len(questions):
        return redirect(url_for("quiz_end"))

    question = questions[index]

    if request.method == "POST":
        selected = request.form.get("answer")
        feedback, correct = check_answer(question, selected)
        # Prepare hint only when the answer is incorrect
        result = {}
        if not correct:
            result["hint"] = get_hint(question)
        else:
            result["hint"] = None

        # Track performance for adaptive difficulty
        update_performance(question["topic"], bool(correct))

        session["quiz_feedback"] = feedback
        session["quiz_result"] = result
        session["quiz_answered"] = True
        session["quiz_correct"] = bool(correct)

        if correct:
            session["quiz_score"] = session.get("quiz_score", 0) + 1

        return redirect(url_for("quiz"))

    # GET render
    feedback = session.pop("quiz_feedback", None)
    result = session.pop("quiz_result", {})
    answered = session.pop("quiz_answered", False)
    was_correct = session.pop("quiz_correct", False)

    display_text = _clean_label_prefix(question.get("text", ""))
    hide_difficulty = bool(session.get("quiz_difficulty_filter"))
    return render_template(
        "quiz.html",
        question=question,
        display_text=display_text,
        feedback=feedback,
        result=result,
        answered=answered,
        was_correct=was_correct,
        hide_difficulty=hide_difficulty,
        explanation=question.get("explanation"),   # <-- ADD THIS
        adaptive=session.get("adaptive", False)
)



@app.route("/quiz/start", methods=["POST"])
def quiz_start():
    count = int(request.form.get("count", 5))
    difficulty = request.form.get("difficulty", "")
    topic = request.form.get("topic", "")

    # Detect adaptive mode
    adaptive = request.form.get("adaptive") == "on"
    session["adaptive"] = adaptive

    if adaptive:
        difficulty = get_adaptive_difficulty(topic)

    qs = get_random_questions(count, topic, difficulty)
    session["quiz_questions"] = qs
    session["quiz_index"] = 0
    session["quiz_score"] = 0
    session["quiz_total"] = len(qs)
    session["quiz_started"] = True
    session["quiz_difficulty_filter"] = difficulty

    return redirect(url_for("quiz"))


@app.route("/quiz/next", methods=["POST"])
def quiz_next():
    session["quiz_index"] = session.get("quiz_index", 0) + 1
    return redirect(url_for("quiz"))


@app.route("/quiz/end")
def quiz_end():
    score = session.get("quiz_score", 0)
    total = session.get("quiz_total", 0)
    percentage = round((score / total) * 100, 1) if total > 0 else 0

    summary = {"score": score, "total": total, "percentage": percentage}
    session.clear()
    return render_template("quiz_end.html", summary=summary)


# -------------------------
# FLASHCARDS (Review)
# -------------------------
@app.route("/review")
def review_page():
    return render_template("review.html")


@app.route("/review_data")
def review_data():
    topic = request.args.get("topic", "").strip()
    difficulty = request.args.get("difficulty", "").strip()

    topic = topic.replace("&amp;", "&")

    with open("questions_full_200.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    def clean_text(t):
        return re.sub(r"^\[[^\]]+\]\s*", "", t or "")

    cards = []
    for q in data:
        ans_letter = q.get("answer", "A")
        index = ord(ans_letter) - 65
        options = q.get("options", [])
        answer_text = options[index] if 0 <= index < len(options) else ""

        cards.append({
            "question": clean_text(q.get("question", "")),
            "answer": answer_text,
            "topic": q.get("topic", ""),
            "difficulty": q.get("difficulty", "")
        })

    if topic:
        cards = [c for c in cards if c["topic"] == topic]
    if difficulty:
        cards = [c for c in cards if c["difficulty"] == difficulty]

    return jsonify(cards[:120])


# -------------------------
# Errors
# -------------------------
@app.errorhandler(404)
def not_found(e):
    return render_template("errors/404.html"), 404


# -----------------------------
# LOGIC MAZE GAME ROUTES
# -----------------------------
@app.route("/logic_maze", methods=["GET", "POST"])
def logic_maze():
    return handle_room_logic(request)


@app.route("/logic_maze/reset")
def logic_maze_reset():
    return reset_maze()


def init_maze_state():
    session["maze_state"] = {
        "current_room": "A",
        "score": 0,
        "mistakes": 0,
        "start_time": datetime.now().timestamp(),
    }


def load_maze():
    with open("maze_rooms.json", "r", encoding="utf-8") as f:
        return json.load(f)


def handle_room_logic(request):
    if "maze_state" not in session:
        init_maze_state()

    state = session["maze_state"]
    maze = load_maze()
    current_room = state["current_room"]

    if current_room == "END":
        total_time = datetime.now().timestamp() - state["start_time"]
        return render_template(
            "maze_end.html",
            score=state["score"],
            mistakes=state["mistakes"],
            time=round(total_time, 2),
        )

    room_data = maze[current_room]

    if request.method == "POST":
        choice = request.form.get("choice")
        if choice == room_data["correct"]:
            state["score"] += 10
            state["current_room"] = room_data["next"]
        else:
            state["mistakes"] += 1
            state["score"] -= 3

        session["maze_state"] = state
        return redirect("/logic_maze")

    return render_template(
        "maze_room.html",
        room=room_data,
        score=state["score"],
        mistakes=state["mistakes"],
    )


def reset_maze():
    session.pop("maze_state", None)
    return redirect("/logic_maze")


if __name__ == "__main__":
    app.run(debug=True)
