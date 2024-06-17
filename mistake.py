from surveys import surveys
from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension

responses = []

app = Flask(__name__)

app.config["SECRET_KEY"] = "oh-so-secret"
debug = DebugToolbarExtension(app)


@app.route("/")
def homepage():
    title = surveys["satisfaction"].title
    instructions = surveys["satisfaction"].instructions
    return render_template("base.html", title=title, instructions=instructions, i=0)


# Accessing `questions[i]` before checking if `i` is within the valid range
@app.route("/questions/<int:i>")
def question(i):

    questions = surveys["satisfaction"].questions
    question = questions[i].question
    choices = questions[i].choices
    if i < len(questions):
        i += 1
        return render_template(
            "questions.html", question=question, choices=choices, i=i
        )
    return render_template("answer.html")
