import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from helpers import error, login_required, recognize, match


UPLOAD_FOLDER = './assets'
ALLOWED_EXTENSIONS = {'webm'}

# Configure application
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///assets/tonguetwister.db")


def user_score():
    """Return user score"""

    rows = db.execute("SELECT score FROM users WHERE id = :userId;", 
                        userId=session["user_id"]) 

    return rows[0]["score"]


def calc_user_score():
    """Calculate a score with the user score"""

    user = db.execute("SELECT AVG(score) AS score FROM history WHERE users_id = :userId;", 
                userId=session["user_id"])

    if user and user[0]["score"]:
        return user[0]["score"]

    return 0.0


def disable_previous():
    """Return true in case of previous phrase is disabled; otherwise false"""

    return session["phrase_id"] == 1


def disable_next():    
    """Return true in case of next phrase is disabled; otherwise false"""

    last_user_phrase = db.execute("SELECT MAX(phrases_id) AS last_phrase_id FROM history WHERE users_id = :users_id;", 
                                    users_id=session["user_id"])

    if last_user_phrase and last_user_phrase[0]["last_phrase_id"]:
        last_phrase_available = db.execute("SELECT MAX(id) AS last_phrase_id FROM phrases;")  
        
        return (session["phrase_id"] == last_phrase_available[0]["last_phrase_id"]) or (session["phrase_id"] == (last_user_phrase[0]["last_phrase_id"]+1))

    return True


def allowed_file(filename):
    """Check id a file name is allowed"""

    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
@login_required
def index():
    """Home page"""

    # Get user score 
    total = user_score()
    if total:
        pass
    else:
        total = 0.0

    # Initialize phrase_id
    session["phrase_id"] = 0

    # Get last user phrase
    last_phrase = db.execute("SELECT MAX(phrases_id) AS last_phrase_id FROM history WHERE users_id = :users_id;", 
                                users_id=session["user_id"])
    if last_phrase and last_phrase[0]["last_phrase_id"]:
        session["phrase_id"] = last_phrase[0]["last_phrase_id"]       

    # Get next phrase available
    next_phrase = db.execute("SELECT * FROM phrases WHERE id = :next_phrase_id;", 
                                next_phrase_id=(session["phrase_id"]+1))                             

    # Get last phrase available
    if next_phrase and next_phrase[0]["id"]:
        session["phrase_id"] = session["phrase_id"]+1
    else:
        # Get last user phrase html
        history = db.execute("SELECT * FROM history INNER JOIN phrases p ON p.id = phrases_id \
                                WHERE users_id = :users_id AND phrases_id = :phrase_id;",
                                users_id=session["user_id"], phrase_id=session["phrase_id"])

        if history and history[0]["original_phrase_html"]:
            original_phrase = {}
            original_phrase["phrase"] = history[0]["original_phrase_html"]

            return render_template("index.html", 
                                    message=history[0]["user_speech_html"], 
                                    total="{total:.1f}%".format(total=user_score()),
                                    score="{score:.1f}%".format(score=history[0]["score"]),
                                    phrase=original_phrase,
                                    disablePrevious=disable_previous(),
                                    disableNext=disable_next())

    return render_template("index.html", 
                            message="#", 
                            total="{total:.1f}%".format(total=total),
                            phrase=next_phrase[0],
                            disablePrevious=disable_previous(),
                            disableNext=disable_next()) 
    

@app.route("/history", methods=["GET", "POST"])
@login_required
def history():
    """History of all user phrases"""
    
    if request.method == "POST":
        db.execute("DELETE FROM history WHERE users_id = :users_id;",
                    users_id=session["user_id"])
        # Updating user score    
        db.execute("UPDATE users SET score = :score WHERE id = :user_id;", 
                    score=0.0, user_id=session["user_id"]) 

    if request.args.get("item"):
        session["phrase_id"] = int(request.args.get("item"))
    
        history = db.execute("SELECT * FROM history INNER JOIN phrases p ON p.id = phrases_id \
                                WHERE users_id = :users_id AND phrases_id = :phrase_id;",
                                users_id=session["user_id"], phrase_id=session["phrase_id"])

        if history and history[0]["original_phrase_html"]:
            original_phrase = {}
            original_phrase["phrase"] = history[0]["original_phrase_html"]

            return render_template("index.html", 
                                    message=history[0]["user_speech_html"], 
                                    total="{total:.1f}%".format(total=user_score()),
                                    score="{score:.1f}%".format(score=history[0]["score"]),
                                    phrase=original_phrase,
                                    disablePrevious=disable_previous(),
                                    disableNext=disable_next())

    history = db.execute("SELECT * FROM history INNER JOIN phrases p ON p.id = phrases_id WHERE users_id = :users_id;", 
                        users_id=session["user_id"])

    return render_template("history.html", history=history)


@app.route("/next", methods=["GET"])
@login_required
def next():
    """Go to next phrase available"""

    last_phrase = db.execute("SELECT MAX(phrases_id) AS last_phrase_id FROM history WHERE users_id = :users_id;", 
                                users_id=session["user_id"])

    if last_phrase and last_phrase[0]["last_phrase_id"] and session["phrase_id"] < last_phrase[0]["last_phrase_id"]:
        session["phrase_id"] = session["phrase_id"] + 1
    
        history = db.execute("SELECT * FROM history INNER JOIN phrases p ON p.id = phrases_id \
                                WHERE users_id = :users_id AND phrases_id = :phrase_id;",
                                users_id=session["user_id"], phrase_id=session["phrase_id"])

        if history and history[0]["original_phrase_html"]:
            original_phrase = {}
            original_phrase["phrase"] = history[0]["original_phrase_html"]

            return render_template("index.html", 
                                    message=history[0]["user_speech_html"], 
                                    total="{total:.1f}%".format(total=user_score()),
                                    score="{score:.1f}%".format(score=history[0]["score"]),
                                    phrase=original_phrase,
                                    disablePrevious=disable_previous(),
                                    disableNext=disable_next()) 

    return redirect("/")  


@app.route("/previous", methods=["GET"])
@login_required
def previous():
    """Return to previous phrase available"""

    if session["phrase_id"] > 1:
        session["phrase_id"] = session["phrase_id"] - 1
    
        history = db.execute("SELECT * FROM history INNER JOIN phrases p ON p.id = phrases_id \
                                WHERE users_id = :users_id AND phrases_id = :phrase_id;",
                                users_id=session["user_id"], phrase_id=session["phrase_id"])

        if history and history[0]["original_phrase_html"]:
            original_phrase = {}
            original_phrase["phrase"] = history[0]["original_phrase_html"]

            return render_template("index.html", 
                                    message=history[0]["user_speech_html"], 
                                    total="{total:.1f}%".format(total=user_score()),
                                    score="{score:.1f}%".format(score=history[0]["score"]),
                                    phrase=original_phrase,
                                    disablePrevious=disable_previous(),
                                    disableNext=disable_next()) 

    return redirect("/")


@app.route("/check", methods=["GET", "POST"])
@login_required
def check():
    """Convert and check audio to text, and calculate user score"""

    result = None
    speech = None
    score = 0
    
    # Get original phrase
    phrase = db.execute("SELECT phrase FROM phrases WHERE id = :phrase_id;", 
                        phrase_id=session["phrase_id"])
    phrase = phrase[0]["phrase"]                        

    # Converting file
    if 'file' not in request.files:
        speech = 'No file part'
    else:
        file = request.files['file']
        if file.filename == '':
            speech = 'No selected file'
        elif file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Recognizing audio
            speech = recognize()

            if speech is None:
                speech = 'Could not understand the audio. You can try again.'

                return jsonify(
                    phrase=phrase,
                    speech=speech,
                    score="{score:.1f}%".format(score=score),
                    total="{total:.1f}%".format(total=user_score())
                )
            else:
                result = match(phrase.lower(), speech.lower())
                score = result.quick_ratio() * 100

    # formatting html
    matching_blocks = result.get_matching_blocks()
    phrase_html = ''
    speech_html = ''
    last_size_a = 0
    last_size_b = 0

    for block in matching_blocks:
        # phrase
        start = block.a
        end = start + block.size
        diff = start - last_size_a
        last_size_a = start + block.size
        if diff > 0:
            phrase_html = phrase_html + "<strong style='color: red;'>" + phrase[(start-diff):start] + "</strong>"
        phrase_html = phrase_html + phrase[start:end]        

        # speech
        start = block.b
        end = start + block.size
        diff = start - last_size_b
        last_size_b = start + block.size
        if diff > 0:
            speech_html = speech_html + "<strong style='color: red;'>" + speech[(start-diff):start] + "</strong>"
        speech_html = speech_html + speech[start:end]  
    
    history = db.execute("SELECT * FROM history WHERE users_id = :user_id AND phrases_id = :phrase_id;",
                user_id=session["user_id"], phrase_id=session["phrase_id"])

    if history and history[0]["phrases_id"]:
        # Update history
        db.execute("UPDATE history SET user_speech = :user_speech, user_speech_html = :user_speech_html, \
                    original_phrase_html = :original_phrase_html, score = :score \
                    WHERE users_id = :user_id AND phrases_id = :phrase_id;", 
                    user_id=session["user_id"], phrase_id=session["phrase_id"], user_speech=speech, \
                        user_speech_html=speech_html, original_phrase_html=phrase_html, score=score) 
        # Recalculate user score
    else:
        # Insert new history
        db.execute("INSERT INTO history (users_id, phrases_id, user_speech, user_speech_html, original_phrase_html, score) \
                    VALUES (:user_id, :phrase_id, :user_speech, :user_speech_html, :original_phrase_html, :score);", 
                    user_id=session["user_id"], phrase_id=session["phrase_id"], user_speech=speech, \
                        user_speech_html=speech_html, original_phrase_html=phrase_html, score=score) 

    # Calculate user score
    total = calc_user_score()

    # Updating user score    
    db.execute("UPDATE users SET score = :score WHERE id = :user_id;", 
                score=total, user_id=session["user_id"]) 

    return jsonify(
        phrase=phrase_html,
        speech="You said: " + speech_html,
        score="{score:.1f}%".format(score=score),
        total="{total:.1f}%".format(total=total)
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return error("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return error("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return error("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return error("must provide username", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists
        if len(rows) > 0:
            return error("this username already exists", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return error("must provide password", 403)

        # Ensure password was submitted (again)
        elif not request.form.get("passwordAgain"):
            return error("must provide password (again)", 403)

        # Ensure password and password again are the same
        elif request.form.get("passwordAgain") != request.form.get("password"):
            return error("password must be the same as password (again)", 403)

        username = request.form.get("username")
        password = generate_password_hash(request.form.get("password"))
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :password)",
                   username=username, password=password)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=username)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/instructions", methods=["GET"])
def instructions():
    """Instructions to the user"""

    return render_template("instructions.html")


def errorhandler(e):
    """Handle error"""

    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return error(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == '__main__':
    app.run(debug=True)
