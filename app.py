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


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
