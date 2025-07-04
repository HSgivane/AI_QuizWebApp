from flask import Flask, request, render_template, redirect, url_for, session
from database.database import *
from config import get_prompt_score, get_prompt_test
from parser import parse_test
from datetime import datetime
from model import ask_openrouter
from dotenv import load_dotenv
import uuid, os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "super-secret-key")

db_create()

@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login = request.form["username"]
        password = request.form["password"]
        if authenticate_user(login, password):
            user_id = get_user_id_by_login(login)
            session["user_id"] = user_id
            return redirect(url_for("profile"))
        else:
            return render_template("login.html", error="Неверный логин или пароль")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        login = request.form["login"]
        username = request.form["username"]
        password = request.form["password"]
        user_id = register_user(login, username, password)
        session["user_id"] = user_id
        return redirect(url_for("profile"))
    return render_template("reg.html")

@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    user = get_user_by_id(session["user_id"])
    if not user:
        return redirect(url_for("logout"))
    
    reg_time = datetime.fromtimestamp(user["reg_time"]).strftime("%d.%m.%Y")
    avatar_filename = f"{user['ava']}.jpg"
    
    test_history = get_user_tests(user["user_id"])

    return render_template("user.html",
                           username=user["user_name"],
                           reg_time=reg_time,
                           avatar_filename=avatar_filename,
                           test_history=test_history)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/test", methods=["GET", "POST"])
def test():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user = get_user_by_id(session["user_id"])
    if not user:
        return redirect(url_for("logout"))

    avatar_filename = f"{user['ava']}.jpg"
    username = user["user_name"]

    if request.method == "POST":
        topic = request.form.get("topic", "").strip()
        if topic:
            session["topic"] = topic
            prompt_test = get_prompt_test(topic)
            print(topic)
            result = ask_openrouter(prompt_test)
            print(result)
            parsed = parse_test(result)
            print(parsed)
            session["parsed_test"] = parsed
            return redirect(url_for("quiz"))
        else:
            error = "Введите тему для генерации теста."
            return render_template("model.html",
                                   username=username,
                                   avatar_filename=avatar_filename,
                                   result="",
                                   error=error)

    return render_template("model.html",
                           username=username,
                           avatar_filename=avatar_filename)

@app.route("/quiz")
def quiz():
    if "user_id" not in session or "parsed_test" not in session:
        return redirect(url_for("login"))

    user = get_user_by_id(session["user_id"])
    if not user:
        return redirect(url_for("logout"))

    avatar_filename = f"{user['ava']}.jpg"
    username = user["user_name"]
    questions = session["parsed_test"]

    return render_template("quiz.html",
                           username=username,
                           avatar_filename=avatar_filename,
                           questions=questions)

@app.route("/score", methods=["POST"])
def score():
    if "user_id" not in session or "parsed_test" not in session:
        return redirect(url_for("login"))

    user = get_user_by_id(session["user_id"])
    if not user:
        return redirect(url_for("logout"))

    questions = session["parsed_test"]
    correct_count = 0

    correct_questions = []
    incorrect_questions = []

    for i, q in enumerate(questions):
        user_answer = request.form.get(f"q{i}")
        correct_answer = request.form.get(f"correct_{i}")
        if user_answer and user_answer == correct_answer:
            correct_count += 1
            correct_questions.append(q["question"])
        else:
            incorrect_questions.append(q["question"])

    session["wrong_questions"] = incorrect_questions

    topic = session.get("topic", "Без темы")
    save_test_result(session["user_id"], topic, correct_count, 10)

    prompt_score = get_prompt_score(correct_questions, incorrect_questions)
    ai_feedback = ask_openrouter(prompt_score)

    return render_template("score.html",
                           username=user["user_name"],
                           avatar_filename=f"{user['ava']}.jpg",
                           total=len(questions),
                           correct=correct_count,
                           wrong_questions=incorrect_questions,
                           ai_feedback=ai_feedback)

@app.route("/upload_avatar", methods=["POST"])
def upload_avatar():
    if "user_id" not in session:
        return redirect(url_for("login"))

    file = request.files.get("avatar")
    if not file or not file.filename.lower().endswith(".jpg"):
        return redirect(url_for("profile"))

    filename = f"{uuid.uuid4().hex}.jpg"
    filepath = os.path.join("static", "avatars", filename)
    file.save(filepath)

    update_avatar_filename(session["user_id"], filename.replace(".jpg", ""))

    return redirect(url_for("profile"))


if __name__ == "__main__":
    app.run(debug=True)
