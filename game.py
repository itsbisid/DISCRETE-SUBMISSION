# game.py — Logic Maze Engine
# Make sure to import this into app.py

import json
from datetime import datetime
from flask import session, redirect, render_template


def init_maze_state():
    """Initialize a new maze game state."""
    session["maze_state"] = {
        "current_room": "A",
        "score": 0,
        "mistakes": 0,
        "start_time": datetime.now().timestamp(),
    }


def load_maze():
    """Load the maze room definitions from JSON."""
    with open("maze_rooms.json", "r") as f:
        return json.load(f)


def handle_room_logic(request):
    """Main handler for processing a move inside the maze."""

    # If first time entering game
    if "maze_state" not in session:
        init_maze_state()

    maze = load_maze()
    state = session["maze_state"]
    current_room = state["current_room"]

    # --- If final room reached ---
    if current_room == "END":
        finish_time = datetime.now().timestamp() - state["start_time"]

        return render_template(
            "maze_end.html",
            score=state["score"],
            mistakes=state["mistakes"],
            time=round(finish_time, 2),
        )

    room_data = maze[current_room]

    # --- Handle POST answer submission ---
    if request.method == "POST":
        choice = request.form.get("choice")

        # correct answer increases score + moves to next room
        if choice == room_data["correct"]:
            state["score"] += 10
            state["current_room"] = room_data["next"]
        else:
            state["mistakes"] += 1
            state["score"] -= 3

        session["maze_state"] = state
        return redirect("/logic_maze")

    # --- Render room ---
    return render_template(
        "maze_room.html",
        room=room_data,
        score=state["score"],
        mistakes=state["mistakes"],
    )


def reset_maze():
    """Reset the entire game state."""
    session.pop("maze_state", None)
    return redirect("/logic_maze")
