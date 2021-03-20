import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


# Home Route
@app.route("/")
@app.route("/home")
def home():
    # Confirms for a Current Session User.
    if "user" in session:
        user = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
        return render_template(
            "home.html", user=user)
    else:
        return render_template("home.html")


# About Route
@app.route("/about")
def about():
    return render_template("about.html")


# Registration Route
@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == 'POST':
        # Confirms for an Existing Username.
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Sorry, That Username's Been Taken.")
            return redirect(url_for("registration"))

        password = request.form.get("password")
        pw_check = request.form.get("confirm-password")
        username = request.form.get("user")

        if password != pw_check:
            flash("That Password's Not Right, Try Again.")

        if password == username:
            flash("Is That the Right Password for This Account?")

        if password == pw_check:

            registration = {
                "username": request.form.get("username").lower(),
                "password": generate_password_hash(
                    request.form.get("password"))
            }

        mongo.db.users.insert_one(registration)

        # Enters the New User into a Session.
        session["user"] = request.form.get("username").lower()
        flash("Hey There {}. Ready to Write?".format(
            request.form.get("username").capitalize()))
        return redirect(url_for(
            "profile", username=session["user"]))
    return render_template("registration.html")


# Sign In Route
@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        # Confirms for an Existing Username.
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # Confirms Password Matches User's.
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                return redirect(url_for(
                    "profile", username=session["user"]))
            else:
                # Confirms Incorrect Password Inputted
                flash("Sorry, Something's Not Right")
                return redirect(url_for("signin"))

        else:
            # Non-Existent Username
            flash("Sorry, Something's Not Right")
            return redirect(url_for("signin"))

    return render_template("signin.html")


# Sign Out Route
@app.route("/signout")
def signout():
    # Removes User from Session Cookie
    flash("Goodbye! See You Again Soon.")
    session.pop("user")
    return redirect(url_for("signin"))


# Profile Route
@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # Obtains User's Session Data from MongoDB.
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template(
            "profile.html", username=username)

    return redirect(url_for("signin"))


# New Entry Route
@app.route("/add_entry", methods=["GET", "POST"])
def add_entry():
    if not session.get("user"):
        return redirect(url_for("error_handler.html"))

    if request.method == "POST":
        complete_sol = "on" if request.form.get("complete_sol") else "off"
        entry = {
            "mood_name": request.form.get("mood_name"),
            "event": request.form.get("event"),
            "severity": request.form.get("severity"),
            "solution": request.form.get("solution"),
            "self_help": request.form.get("self_help"),
            "activity_dur": request.form.get("activity_dur"),
            "complete_sol": complete_sol,
            "created_by": session["user"],
            "date": request.form.get("date")
        }
        mongo.db.entries.insert_one(entry)
        return redirect(url_for('collate_entries'))

    moods = mongo.db.moods.find().sort("mood_name", 1)
    return render_template("new_entry.html", moods=moods)


# More Information Route
@app.route("/more_info/<entry_id>")
def more_info(entry_id):
    entry = mongo.db.entries.find_one({"_id": ObjectId(entry_id)})
    return render_template("more_info.html", entry=entry)


# Edit Entry Route
@app.route("/edit_entry/<entry_id>", methods=["GET", "POST"])
def edit_entry(entry_id):
    if not session.get("user"):
        return redirect(url_for("error_handler"))

    if request.method == "POST":
        complete_sol = "on" if request.form.get(
            "complete_sol") else "off"
        updatedEntry = {
            "mood_name": request.form.get("mood_name"),
            "event": request.form.get("event"),
            "severity": request.form.get("severity"),
            "solution": request.form.get("solution"),
            "self_help": request.form.get("self_help"),
            "activity_dur": request.form.get("activity_dur"),
            "complete_sol": complete_sol,
            "created_by": session["user"],
            "date": request.form.get("date")
        }
        mongo.db.entries.update({"_id": ObjectId(entry_id)}, updatedEntry)

    entry = mongo.db.entries.find_one({"_id": ObjectId(entry_id)})
    moods = mongo.db.moods.find().sort("mood_name", 1)
    return render_template("edit_entry.html", entry=entry, moods=moods)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
