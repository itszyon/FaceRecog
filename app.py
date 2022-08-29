import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

# Start application
app = Flask(__name__)

# Configure session for app
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Include database
db = SQL("sqlite:///facerecognition.db")

# Check if API_KEY is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

# Check if the user has loged in
def login_required(f):
    """
    Decorate routes to require login.
    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def apology(text):
    return render_template("apology.html", text=text)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def homepage():
    # TODO

    return

@app.route("/login", methods=["GET", "POST"])
def login():
    # TODO
    
    session.clear()

    if request.method == "POST":

        # Retrieve the information from the user
        username = request.form.get("username")
        password = request.form.get("password")

        # Check if the user has provided data
        if not username:
            return apology("Please introduce a username")
        elif not password:
            return apology("Please introduce a password")
        
        row = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(row) != 1:
            return apology("Invalid username")
        
        if password != check_password_hash(row[0]["hash"], password):
            return apology("Wrong password")
        
        session["user_id"] = row[0]["id"]

        return redirect("/index")

    else:
        return render_template("login.html")
        

@app.route("/register", methods=["GET", "POST"])
def register():
    # TODO

    session.clear()

    if request.method == "POST":

        # Retrieve the information from the user
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Look up all usernames in database
        rows = db.execute("SELECT username FROM users")

        if password != confirmation:
            return apology("Make sure you have introduced the correct password")

        # Check if the username introduced by the new user already exists
        for row in rows:
            if username == row["username"]:
                return apology("Username already exists")

        # Create a hash for the users' password
        hash = generate_password_hash(password)

        # Introduce new username and hashed password into the database
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)

        # Initialize session for the new user
        row = db.execute("SELECT id FROM users WHERE username = ?", username)
        session["user_id"] = row[0]["id"]

        # Redirect to homepage
        return redirect("/index")
    
    # If the user accesses through GET show the page
    else:
        return render_template("register.html")


@app.route("/index")
@login_required
def index():
    # TODO

    return

@app.route("/facerecognition")
@login_required
def facerecognition():
    # TODO

    return

@app.route("/uploadfaces")
@login_required
def uploadfaces():
    # TODO

    return

@app.route("/faceidentification")
@login_required
def faceidentification():
    # TODO

    return
