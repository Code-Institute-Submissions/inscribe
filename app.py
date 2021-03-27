import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for, abort)
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
    if request.method == "POST":
        # Confirms for Existing Username
        registered_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if registered_user:
            flash("Sorry, That Username's Been Taken.")
            return redirect(url_for("registration"))

        password = request.form.get("password")
        pw_check = request.form.get("confirm-password")

        # Cross-checks Password with Inputted Confirm Password.
        if password != pw_check:
            flash("Something's Not Right, Try Again.")
            return redirect(url_for("registration"))

        # Confirm if Password and Confirm Password are the Same.
        if password == pw_check:

            new_user = {
                "username": request.form.get("username").lower(),
                "password": generate_password_hash(
                    request.form.get("password").lower()),
                    }

        mongo.db.users.insert_one(new_user)

        session["user"] = request.form.get("username").lower()
        flash("Welcome to (in)Scribe. Ready to Write?")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("registration.html")


# Sign-In Route
@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        # Confirms for Existing Username
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # Confirms Hashed Password Aligns with Users Input.
            if check_password_hash(
                existing_user["password"],
                    request.form.get("password")) and check_password_hash(
                existing_user["password"],
                    request.form.get("confirm-password")):
                session["user"] = request.form.get("username").lower()
                flash("Hey There {}. Ready to Write?".format(
                    request.form.get("username").capitalize()))
                return redirect(url_for(
                    "profile", username=session["user"]))
            else:
                # Incorrect Password Inputted
                flash("Sorry, Something's Not Right")
                return redirect(url_for("signin"))

        else:
            # Username Doesn't Yet Exist.
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


@app.route("/profile/<username>")
def profile(username):
    try:
        if not session.get("user"):
            return redirect(url_for("signin"))
        else:
            username = mongo.db.users.find_one(
                {"username": session["user"]})["username"]
            return render_template("profile.html", username=username)
# Prevents KeyError from Stopping the Return of User's Profile When Signed In.
    except KeyError:
        return render_template("profile.html", username=username)


# New Entry Route
@app.route("/add_entry", methods=["GET", "POST"])
def add_entry():
    if not session.get("user"):
        abort(404)

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
@app.route("/more_info/<entry_id>", methods=["GET"])
def more_info(entry_id):
    if not session.get("user"):
        abort(403)

    entry = mongo.db.entries.find_one({"_id": ObjectId(entry_id)})
    return render_template("more_info.html", entry=entry)


# Edit Entry Route
@app.route("/edit_entry/<entry_id>", methods=["GET", "POST"])
def edit_entry(entry_id):
    if not session.get("user"):
        abort(403)

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


# Delete Entry Route
@app.route("/delete_entry/<entry_id>")
def delete_entry(entry_id):
    if not session.get("user"):
        return redirect(url_for('error_handler'))

    mongo.db.entries.delete_one({"_id": ObjectId(entry_id)})
    return redirect(url_for("collate_entries"))


# Search Functionality Route
@app.route("/search", methods=["GET", "POST"])
def search():
    if not session.get("user"):
        abort(403)

    query = request.form.get("query")
    entries = list(mongo.db.entries.find({"$text": {"$search": query}}))
    return render_template("search.html", entries=entries)


# All Entries Route
@app.route("/collate_entries", methods=["GET"])
def collate_entries():
    try:
        if not session.get("user"):
            return redirect(url_for("signin"))
        else:
            # Obtains User's Session Data from MongoDB.
            username = mongo.db.users.find_one(
                {"username": session["user"]})["username"]
            # Obtains User's Entry Data from MongoDB.
            entries = list(mongo.db.entries.find())
            return render_template(
                "entries.html", username=username, entries=entries)
    except KeyError:
        return render_template(
            "entries.html", username=username, entries=entries)


# Community Route
@app.route("/community_home", methods=["GET"])
def community_home():
    if not session.get("user"):
        return redirect(url_for("error_handler.html"))

    suggestions = list(mongo.db.suggestions.find())
    return render_template("community.html", suggestions=suggestions)


# Edit Suggestion Route
@app.route("/edit_sugg/<suggestion_id>", methods=["GET", "POST"])
def edit_sugg(suggestion_id):
    if not session.get("user"):
        abort(403)

    if request.method == "POST":
        updatedSugg = {
            "suggestion_name": request.form.get("suggestion_name"),
            "suggestion_desc": request.form.get("suggestion_desc"),
            "sugg_date": request.form.get("sugg_date"),
            "reason": request.form.get("reason"),
            "created_by": session["user"],
        }
        mongo.db.suggestions.update_one(
            {"_id": ObjectId(suggestion_id)}, updatedSugg)

    suggestion = mongo.db.suggestions.find_one(
        {"_id": ObjectId(suggestion_id)})
    return render_template("edit_sugg.html", suggestion=suggestion)


# New Suggestion Route
@app.route("/add_sugg", methods=["GET", "POST"])
def add_sugg():
    if not session.get("user"):
        abort(403)

    if request.method == "POST":
        suggestion = {
            "suggestion_name": request.form.get("suggestion_name"),
            "suggestion_desc": request.form.get("suggestion_desc"),
            "sugg_date": request.form.get("sugg_date"),
            "reason": request.form.get("reason"),
            "created_by": session["user"],
        }
        mongo.db.suggestions.insert_one(suggestion)
        return redirect(url_for('community_home'))

    return render_template("add_sugg.html")


# Delete Entry Route
@app.route("/delete_sugg/<suggestion_id>")
def delete_sugg(suggestion_id):
    if not session.get("user"):
        return redirect(url_for('error_handler'))

    mongo.db.suggestions.delete_one({"_id": ObjectId(suggestion_id)})
    return redirect(url_for("community_home"))


# Error Handling / Routes

@app.errorhandler(403)
def forbidden(e):
    return render_template("403.html"), 403


@app.errorhandler(404)
def no_content(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(host=os.environ.get("IP", "0.0.0.0"),
            port=int(os.environ.get("PORT", "5000")),
            debug=True)
