from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import *

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
debug = DebugToolbarExtension(app)

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


response = []


@app.route("/")
def start_survey():
    sat = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template("/index.html", sat=sat, instructions=instructions)

@app.route("/session", methods=["POST"])
def sess_resp():
    session['responses'] = []
    return redirect("/questions/0")


number = 0


@app.route("/questions/<int:num>")
def quest(num):
    if len(session['responses']) == num:
        q = satisfaction_survey.questions[num]
        global number
        number = num
        return render_template("questions.html", q=q)
    else:
        if number < len(satisfaction_survey.questions) - 1:
            flash("Please answer the questions in order!", "error")
            return redirect(f"/questions/{len(response)}")
        else:
            return redirect("/thanks")


@app.route("/answer", methods=["POST"])
def ans():
    print(request.form)
    response = session['responses']
    re = request.form.get("choice")
    response.append(re)
    session['responses'] = response
    print(response)

    if number < len(satisfaction_survey.questions) - 1:
        return redirect(f"/questions/{number+1}")
    else:
        return redirect("/thanks")
    return "test"


@app.route("/thanks")
def last_ans():
    print(response)
    return render_template("thanks.html")
