import json
import random
import os

# -------------------------------------------------
# Load question bank safely using absolute path
# -------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUESTIONS_PATH = os.path.join(BASE_DIR, "questions_full_200.json")

with open("questions_full_200.json", "r", encoding="utf-8") as f:
    QUESTIONS = json.load(f)

# -------------------------------------------------
# Return a list of random questions
# -------------------------------------------------

def get_random_questions(count=10, topic=None, difficulty=None):
    filtered = QUESTIONS
    if topic:
        filtered = [q for q in filtered if q["topic"] == topic]
    if difficulty:
        filtered = [q for q in filtered if q["difficulty"] == difficulty]

    return random.sample(filtered, min(count, len(filtered)))

# -------------------------------------------------
# Check submitted answer
# -------------------------------------------------
def check_answer(question, selected_option):
    # Letter -> index mapping
    letter_to_index = {"A": 0, "B": 1, "C": 2, "D": 3}

    correct_letter = question["answer"].strip()
    correct_index = letter_to_index[correct_letter]

    correct_option_text = question["options"][correct_index].strip()

    # Compare selected option text to correct option text
    correct = (selected_option.strip() == correct_option_text)

    feedback = "✅ Correct!" if correct else f"❌ Incorrect. Correct answer: {correct_option_text}"
    return feedback, correct


# -------------------------------------------------
# Return hint for the current question
# -------------------------------------------------

def get_hint(question):
    return question.get("hint") or "No hint available."
