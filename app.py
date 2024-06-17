from surveys import surveys
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config["SECRET_KEY"] = "oh-so-secret"
debug = DebugToolbarExtension(app)

app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False


@app.route("/")
def homepage():
    title = surveys["satisfaction"].title
    instructions = surveys["satisfaction"].instructions
    return render_template("base.html", title=title, instructions=instructions)


@app.route("/session", methods=["POST"])
def set_session():
    session["responses"] = []
    return redirect(f"/questions/0")


@app.route("/questions/<int:i>")
def question(i):

    questions = surveys["satisfaction"].questions
    responses = session.get("responses")

    if len(responses) == len(questions):
        return redirect("/thank-you")

    if i != len(responses):
        flash("Invalid Question")
        return redirect(f"/questions/{len(responses)}")

    if i < len(questions):
        question = questions[i].question
        choices = questions[i].choices
        return render_template(
            "questions.html",
            question=question,
            choices=choices,
            i=i + 1,
            responses=responses,
        )
    return render_template("thank-you.html")


@app.route("/answer/<int:i>", methods=["POST"])
def answer(i):
    questions = surveys["satisfaction"].questions
    choice = request.form.get("choice")
    responses = session["responses"]
    responses.append(choice)
    session["responses"] = responses  # Reassigning the Session key
    # session.modified = True # Marking the Session as modified
    if len(responses) == len(questions):
        return redirect("/thank-you")
    return redirect(f"/questions/{i}")


@app.route("/thank-you")
def thank_you():
    return render_template("thank-you.html")


# surveys = {
#     "satisfaction": satisfaction_survey,
#     "personality": personality_quiz,
# }

# satisfaction_survey = Survey(
#     "Customer Satisfaction Survey",
#     "Please fill out a survey about your experience with us.",
#     [
#         Question("Have you shopped here before?"),
#         Question("Did someone else shop with you today?"),
#         Question(
#             "On average, how much do you spend a month on frisbees?",
#             ["Less than $10,000", "$10,000 or more"],
#         ),
#         Question("Are you likely to shop here again?"),
#     ],
# )

""" NOTE

SESSIONS

`session` is a way to store information about a user across different request.

    from flask import session

    session['key'] = 'value'  # Storing Data in the Session
    value = session.get('key')  # Retrieving Data from the Session

    session.pop('key', None)  # Removing Data from the Session
    session.clear() # Clearing the Session

Flask needs to be explicitly told that the session has been modified - BE ADVISED THAT MODIFICATION ON MUTABLE STRUCTURES ARE NOT PICKED UP AUTOMATICALLY.

MUTABLE STRUCTURES: 
    - Lists
    - Dictionaries
    - Sets
    - Users-defined Classes



 """
