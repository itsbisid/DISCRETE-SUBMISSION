import json
import os
from flask import (
    Flask, render_template, request, redirect,
    session, url_for, jsonify
)
from datetime import datetime
from logic_engine import (
    normalize_formula,
    truth_table,
    classify_formula,
    check_equivalence,
    check_argument_validity
)

# -----------------------------------------------------
# APP SETUP
# -----------------------------------------------------
app = Flask(__name__)
app.secret_key = "discrete_math_secret_key"

# File paths
USER_FILE = "data/users.json"
QUESTION_FILE = "data/questions.json"
MAZE_FILE = "data/maze.json"

# -----------------------------------------------------
# LOAD JSON HELPERS
# -----------------------------------------------------
def load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

# -----------------------------------------------------
# HOME / LANDING PAGE
# -----------------------------------------------------
@app.route("/")
def home():
    return render_template("setup_project.html")

# -----------------------------------------------------
# AUTH ROUTES
# -----------------------------------------------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        users = load_json(USER_FILE)

        username = request.form.get("username")
        password = request.form.get("password")

        # Check duplicate
        for u in users:
            if u["username"] == username:
                return render_template("signup.html",
                                       error="Username already exists.")

        users.append({
            "username": username,
            "password": password,
            "created": str(datetime.now()),
            "quizzes_taken": 0
        })

        save_json(USER_FILE, users)
        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        users = load_json(USER_FILE)
        username = request.form.get("username")
        password = request.form.get("password")

        for u in users:
            if u["username"] == username and u["password"] == password:
                session["user"] = username
                return redirect(url_for("dashboard"))

        return render_template("login.html",
                               error="Invalid username or password.")

    return render_template("login.html")


@app.route("/guest")
def guest():
    session["user"] = "GUEST"
    return redirect(url_for("dashboard"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

# -----------------------------------------------------
# DASHBOARD
# -----------------------------------------------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("home"))
    return render_template("dashboard.html", user=session["user"])

# -----------------------------------------------------
# LEARNING MODULE
# -----------------------------------------------------
@app.route("/learn")
def learn():
    topics = [
        "Propositional Logic",
        "Truth Tables",
        "Logical Equivalence",
        "Rules of Inference",
        "Predicates & Quantifiers",
        "Sets",
        "Proof Techniques",
        "Boolean Functions",
        "Logic Gates",
        "Algorithms",
        "Induction"
    ]
    return render_template("learn.html", topics=topics)


@app.route("/learn/<topic>")
def learn_topic(topic):
    return render_template("learn_topic.html", topic=topic)

# -----------------------------------------------------
# LOGIC TOOLS
# -----------------------------------------------------
@app.route("/tools", methods=["GET", "POST"])
def tools():
    result = {}
    if request.method == "POST":
        action = request.form.get("action")

        # ------------------------------
        # TRUTH TABLE
        # ------------------------------
        if action == "truth":
            formula = normalize_formula(request.form.get("formula", ""))
            try:
                table = truth_table(formula)
                result["truth_table"] = table
            except:
                result["error"] = "Invalid formula."

        # ------------------------------
        # CLASSIFIER
        # ------------------------------
        elif action == "classify":
            formula = normalize_formula(request.form.get("formula", ""))
            try:
                result["classification"] = classify_formula(formula)
            except:
                result["error"] = "Invalid formula."

        # ------------------------------
        # EQUIVALENCE CHECKER
        # ------------------------------
        elif action == "equivalence":
            f1 = normalize_formula(request.form.get("formula1", ""))
            f2 = normalize_formula(request.form.get("formula2", ""))
            try:
                result["equivalent"] = check_equivalence(f1, f2)
            except:
                result["error"] = "Invalid formula."

        # ------------------------------
        # ARGUMENT VALIDITY CHECKER
        # ------------------------------
        elif action == "validity":
            raw = request.form.get("premises", "")
            conclusion = normalize_formula(request.form.get("conclusion", ""))

            try:
                premises_list = [normalize_formula(x.strip())
                                 for x in raw.split(",")]

                result["validity"] = check_argument_validity(
                    premises_list, conclusion
                )
            except:
                result["error"] = "Invalid argument structure."

    return render_template("tools.html", result=result)

# -----------------------------------------------------
# QUIZ ENGINE
# -----------------------------------------------------
@app.route("/quiz", methods=["GET", "POST"])
def quiz_setup():
    questions = load_json(QUESTION_FILE)
    topics = sorted(list({q["topic"] for q in questions}))

    return render_template("quiz_setup.html", topics=topics)


@app.route("/quiz/start", methods=["POST"])
def quiz_start():
    questions = load_json(QUESTION_FILE)

    num = int(request.form.get("num"))
    difficulty = request.form.get("difficulty")
    topic = request.form.get("topic")

    # Filter
    filtered = [
        q for q in questions
        if (difficulty == "Any" or q["difficulty"] == difficulty)
        and (topic == "Any" or q["topic"] == topic)
    ]

    # Pick num questions
    session["quiz"] = filtered[:num]
    session["index"] = 0
    session["score"] = 0
    session["mistakes"] = 0
    session["start"] = datetime.now().timestamp()

    return redirect(url_for("quiz_question"))


@app.route("/quiz/question", methods=["GET", "POST"])
def quiz_question():
    if "quiz" not in session:
        return redirect(url_for("quiz_setup"))

    quiz = session["quiz"]
    index = session["index"]

    if index >= len(quiz):
        return redirect(url_for("quiz_end"))

    question = quiz[index]

    feedback = None
    explanation = None

    if request.method == "POST":
        selected = request.form.get("choice")
        correct = question["answer"]

        if selected == correct:
            session["score"] += 1
            feedback = "correct"
        else:
            session["mistakes"] += 1
            feedback = "wrong"
            explanation = question.get("explanation", "")

        session["index"] += 1

        return render_template(
            "quiz_question.html",
            question=question,
            feedback=feedback,
            explanation=explanation
        )

    return render_template("quiz_question.html", question=question)

@app.route("/quiz/end")
def quiz_end():
    score = session.get("score", 0)
    mistakes = session.get("mistakes", 0)
    start = session.get("start", 0)

    time_elapsed = int(datetime.now().timestamp() - start)

    # Ranking logic
    if score >= 35:
        rank = "Platinum"
    elif score >= 25:
        rank = "Gold"
    elif score >= 15:
        rank = "Silver"
    else:
        rank = "Bronze"

    return render_template(
        "quiz_end.html",
        score=score,
        mistakes=mistakes,
        time=time_elapsed,
        rank=rank
    )

# -----------------------------------------------------
# LOGIC MAZE GAME
# -----------------------------------------------------
@app.route("/logic_maze")
def maze_start():
    session["maze_room"] = "room1"
    session["maze_score"] = 0
    session["maze_mistakes"] = 0
    session["maze_start"] = datetime.now().timestamp()
    return redirect(url_for("maze_room"))


@app.route("/maze/room", methods=["GET", "POST"])
def maze_room():
    maze = load_json(MAZE_FILE)
    room_id = session.get("maze_room", "room1")
    room = maze[room_id]

    if request.method == "POST":
        choice = request.form.get("choice")
        correct = room["correct"]

        if choice == correct:
            session["maze_score"] += 1
            next_room = room["next"]
            session["maze_room"] = next_room

            if next_room == "end":
                return redirect(url_for("maze_end"))
        else:
            session["maze_mistakes"] += 1

    return render_template("maze_room.html", room=room)


@app.route("/logic_maze/end")
def maze_end():
    score = session.get("maze_score", 0)
    mistakes = session.get("maze_mistakes", 0)
    time_elapsed = int(datetime.now().timestamp() - session.get("maze_start", 0))

    return render_template(
        "maze_end.html",
        score=score,
        mistakes=mistakes,
        time=time_elapsed
    )

# -----------------------------------------------------
# THEME SWITCHER
# -----------------------------------------------------
@app.route("/theme/<mode>")
def theme(mode):
    session["theme"] = mode
    return redirect(request.referrer or url_for("dashboard"))

# -----------------------------------------------------
# RUN APP
# -----------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
