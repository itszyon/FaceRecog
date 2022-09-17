import os
import face_recognition

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from functools import wraps

# Start application
app = Flask(__name__)

# Configure session for app
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["UPLOAD_FOLDER"] = "./static"
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

    return render_template("homepage.html")

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

        if not check_password_hash(row[0]["hash"], password):
            return apology("Wrong password")

        session["user_id"] = row[0]["id"]

        # We have to make sure the user has the necesary folders to store the images

        dir = "./static"
        os.chdir(dir)

        # Check if the data folder exists
        if "data" not in os.listdir():
            os.mkdir("data")
        
        dir = "./data"
        os.chdir(dir)

        # Check if the user has a folder to their name
        if username not in os.listdir():
            os.mkdir(username)

            # Make the directories to store the faces an the gallery
            dir = "./" + username
            os.chdir(dir)
            os.mkdir("faces") 
            os.mkdir("gallery")

            # Make the full_gallery folder in the gallery
            dir = "./gallery/"
            os.chdir(dir)
            os.mkdir("full_gallery")
            dir = "../../../../"
            os.chdir(dir)
        
        # If the user has a folder
        else:
            dir = "./" + username
            os.chdir(dir)
            list = os.listdir()

            # Check if the user has the faces folder
            if "faces" not in list:
                os.mkdir("faces")

            # Check if the user has the gallery folder
            if "gallery" not in list:
                os.mkdir("gallery")
                os.mkdir("./gallery/full_gallery")
            
            dir = "../../../"
            os.chdir(dir)

        return redirect("/index")

    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    # TODO

    session.clear()

    if request.method == "POST":

        # Retrieve the information from the user
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if username == "":
            return apology("Please introduce a username")

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

        dir = "./static/data/" + username
        os.mkdir(dir)

        faces = dir + "/faces"
        os.mkdir(faces)

        gallery = dir + "/gallery"
        os.mkdir(gallery)

        full_gallery = dir + "/gallery/full_gallery"
        os.mkdir(full_gallery)

        # Redirect to homepage
        return redirect("/index")

    # If the user accesses through GET show the page
    else:
        return render_template("register.html")


@app.route("/index")
@login_required
def index():
    # TODO
    # Get users' id
    id = session["user_id"]

    # Get users' username from database
    row = db.execute("SELECT username FROM users WHERE id=?", id)
    username = row[0]["username"]

    # Create a string with the name of the directory we have to access to obtain the users' faces
    directory = "./static/data/" + username + "/faces"

    # Access said directory
    os.chdir(directory)

    # Retrieve the names of all the files in the folder
    list = os.listdir()

    # Go back to the initial directory
    os.chdir("../../../../")

    faces = {}
    for face in list:
        faces[face] = len(face.split(".")[1]) + 1

    return render_template("index.html", faces=faces, username=username)

@app.route("/organisephotos", methods=["GET", "POST"])
@login_required
def organisephotos():
    # TODO
    if request.method == "POST":

        # Retrieve the users' username
        id = session["user_id"]
        row = db.execute("SELECT username FROM users WHERE id = ?", id)
        username = row[0]["username"]

        # Store all the faces in a list
        dir = "./static/data/" + username + "/faces/"
        os.chdir(dir)
        faces = os.listdir()

        # Obtain the image the user has uploaded and check if there is an image
        image = request.files["image"]
        if not image:
            return apology("No image uploaded")

        # Get information about the file
        filename = secure_filename(image.filename)
        img = image.read()

        # Access the direction where we want to save the image
        dir = "../gallery/full_gallery"
        os.chdir(dir)

        # Create a file with the information of the image
        f = open(filename, "wb")
        f.write(img)
        f.close()

        # Encode the image we want to analize
        unknown_image = face_recognition.load_image_file(filename)
        unknown_image_encodings = face_recognition.face_encodings(unknown_image)

        if len(unknown_image_encodings) > 0:
            unknown_image_encoding = unknown_image_encodings[0]
        else:
            dir = "../../../../../"
            os.chdir(dir)
            return redirect("/index")

        # Initialize a variable to store the matches
        results = []

        # Run through all the faces the user has to check if there is a match
        for face in faces:
            # Encode the face we are currently checking
            person = face_recognition.load_image_file("../../faces/" + face)
            person_encoding = face_recognition.face_encodings(person)[0]

            # Compare the new image to the faces
            result = face_recognition.compare_faces([person_encoding], unknown_image_encoding, tolerance=0.70)
            print(result)

            # Add the name of the face to the match list if it is true
            if True in result:
                print(face.split(".")[0])
                results.append(face.split(".")[0])
        
        print(results)
        # Go to gallery directory
        dir = "../"
        os.chdir(dir)

        # Save the image in every folder with th names of the people in it
        for match in results:
            dir = "./" + match
            os.chdir(dir)
            f = open(filename, "wb")
            f.write(img)
            f.close()
            dir = "../"
            os.chdir(dir)

        # Go back to the initial directory
        os.chdir("../../../../")

        return redirect("/index")

    else:
        return render_template("organisephotos.html")

@app.route("/addfaces", methods=["GET", "POST"])
@login_required
def uploadfaces():
    # TODO
    if request.method == "POST":

        # Retrieve the users' username
        id = session["user_id"]
        row = db.execute("SELECT username FROM users WHERE id = ?", id)
        username = row[0]["username"]

        # Obtain the image the user has uploaded and check if there is an image
        face = request.files["face"]
        if not face:
            return apology("No image uploaded")

        # Get information about the file
        filename = secure_filename(face.filename)
        img = face.read()

        # Access the direction where we want to save the image
        dir = "./static/data/" + username + "/faces/"
        os.chdir(dir)

        # Create a file with the information of the image
        f = open(filename, "wb")
        f.write(img)
        f.close()

        # Go back to the initial directory
        os.chdir("../../../../")

        # Create folder in gallery with the name of the image introduced
        name = filename.split(".")
        path = "./static/data/" + username + "/gallery/" + name[0]
        os.mkdir(path)

        return redirect("/index")
    else:
        return render_template("addfaces.html")

@app.route("/viewgallery", methods=["GET", "POST"])
@login_required
def viewgallery():
    # TODO
    if request.method == "POST":
        # Get the users' input
        face = request.form.get("person")

        # Get users' id
        id = session["user_id"]

        # Get users' username from database
        row = db.execute("SELECT username FROM users WHERE id=?", id)
        username = row[0]["username"]

        # Enter the users' gallery
        dir = "./static/data/" + username + "/gallery/"
        os.chdir(dir)

        # Get the list of all the folders of people in the gallery to choose from
        people = os.listdir()

        # Create a string with the name of the directory we have to access to obtain the users' faces
        dir = "./" + face

        # Access said directory
        os.chdir(dir)

        # Retrieve the names of all the files in the folder
        list = os.listdir()

        # Go back to the initial directory
        os.chdir("../../../../../")

        images = {}
        for image in list:
            images[image] = len(image.split(".")[1]) + 1

        return render_template("viewgallery.html", people=people, images=images, username=username, face=face)
    
    else:
        # Get users' information
        id = session["user_id"]
        row = db.execute("SELECT username FROM users WHERE id = ?", id)
        username = row[0]["username"]
        
        # Enter the users' gallery
        dir = "./static/data/" + username + "/gallery/"
        os.chdir(dir)

        # Get the list of all the folders of people in the gallery to choose from
        people = os.listdir()

        # Go back to original directory
        dir = "../../../../"
        os.chdir(dir)

        images = {}
        
        return render_template("viewgallery.html", people=people, images=images, username=username)
