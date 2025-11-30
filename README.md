

# 📘 **Logic Reasoning Tutor**

A Flask-based interactive learning platform for Discrete Mathematics — built for CS221 (Discrete Structures & Theory), Fall 2025.

The app provides an intuitive interface for learning logic, evaluating formulas, generating truth tables, testing argument validity, playing a logic maze game, and taking custom difficulty-based quizzes.
It is designed with accessibility, inclusivity, and modularity in mind, supporting both beginners and advanced logic learners.

---

## 🚀 **Features**

### **1. Logic Tools Suite**

A full set of core tools needed to practice propositional logic:

* ✔ **Truth Table Generator**
* ✔ **Logical Formula Classifier**
  (tautology, contradiction, contingency)
* ✔ **Equivalence Checker**
* ✔ **Argument Validity Checker**
* ✔ **Syntax Normalizer & Error Handling**

  * Catch malformed formulas
  * User-friendly error messages
  * Auto-cleaning spaces, capitalizations, and symbols

---

### **2. Dynamic Quiz System (200 Questions)**

* 200+ curated MCQs across topics in Discrete Math
* Difficulty levels: **Easy**, **Medium**, **Hard**
* Topic filtering: Propositional Logic, Sets, Functions, Quantifiers, Boolean Algebra, Algorithms, etc.
* Hint engine with concept explanations
* Interactive feedback (“Correct!”, “Try Again”, explanations)
* Timer + score tracking
* End-of-quiz performance summary
* Leaderboard-ready user system

---

### **3. Logic Maze Game**

A story-based puzzle sequence where users solve logic questions to move through rooms.

* JSON-based room definitions
* Score + mistakes tracking
* End-game ranking system (Platinum, Gold, Silver, Bronze)
* Visual UI with images + animations
* Progress persistence during session
* Accessible for both beginners and advanced learners

---

### **4. Learning Module**

A clean, structured concept library covering:

* 🧩 Propositional Logic
* 🧮 Truth Tables
* 🖇 Logical Equivalences
* 🔢 Quantifiers
* 🎯 Rules of Inference
* 🔤 Boolean Functions
* 📐 Sets & Functions
* 🧠 Algorithms
* 🔄 Mathematical Induction

Each topic includes:

* definitions
* examples
* notes
* interactive deepen-understanding buttons
* (future) audio/voice module for accessibility

---

### **5. User System**

* Login + logout
* Guest mode
* JSON-based user storage
* Session tracking
* Future-ready for Firebase/Auth/Supabase integrations

---

### **6. Performance Dashboard**

Shows aggregated user progress:

* Quiz accuracy per topic
* Average completion time
* Maze game outcomes
* Streak system
* Personalized recommendations (planned)

---

### **7. UI & Theme System**

* Light, dark, and glassmorphism modes
* Smooth transitions
* Mobile responsiveness
* Tailwind-based styling with custom variables
* Improved accessibility for low-vision users

---

## 🏗 **Tech Stack**

| Component         | Technology                                |
| ----------------- | ----------------------------------------- |
| **Backend**       | Flask (Python), JSON Storage              |
| **Frontend**      | HTML, CSS, Tailwind, JavaScript           |
| **Animations/UI** | CSS transitions, custom JS                |
| **Data**          | question_bank.json, users.json, maze.json |
| **Deployment**    | PythonAnywhere / Render / Local           |

---

## 📂 **Project Structure**

```
LogicTutor/
│
├── app.py                    # Main Flask server
├── static/
│   ├── css/                  # Stylesheets
│   ├── js/                   # Client-side scripts
│   ├── images/               # Maze + UI graphics
│   └── questions/
│       └── question_bank.json
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── learn.html
│   ├── tools.html
│   ├── quiz.html
│   ├── quiz_result.html
│   ├── logic_maze.html
│   └── setup_project.html
│
└── README.md
```

---

## 🔧 **Setup & Installation**

### **1. Clone the repository**

```bash
git clone https://github.com/yourusername/logic-tutor.git
cd logic-tutor
```

### **2. Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### **3. Install dependencies**

```bash
pip install -r requirements.txt
```

### **4. Run the app**

```bash
python app.py
```

Then open:

```
http://localhost:5000
```

---

## 🧪 **Testing**

The app includes:

* Unit tests for logic-parsing functions
* Truth table generation tests
* Checker tests for equivalence & argument validity
* Edge-case handling for syntax errors

Run tests:

```bash
pytest
```

---

## 🌟 **Future Improvements**

Some planned enhancements (based on realistic development priorities):

* Interactive proof builder
* Drag-and-drop logic gates
* SQLite/PostgreSQL backend
* User analytics dashboard with graphs
* Flashcards module
* API for external apps to evaluate logic expressions
* Full accessibility audio guide for deaf/ESL learners

---

## 🤝 **Contributors**

* **Awinbisid Desmond-Bugbilla**
* **Albert Nii Okai Quaye**
* **Kwasi Ampaabeng Kyeremeh**

---

## 📄 **License**

MIT License — free to use, modify, and learn from.

---

## 🎯 Summary

This README reflects your full, feature-rich Logic Reasoning Tutor:
logic tools, quizzes, maze game, learning module, UI themes, and Flask backend.

