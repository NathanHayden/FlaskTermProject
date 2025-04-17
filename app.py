from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_session import Session
import uuid
import os

app = Flask(__name__)
app.secret_key = "password"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
Session(app)

file_save_location = "static/images"
allowed_types = [".png", ".jpg", ".jpeg"]
os.makedirs(file_save_location, exist_ok=True)


@app.before_request
def session_start():
    session.setdefault("sid", str(uuid.uuid4()))
    session.setdefault("items", {})


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/cards")
def view_cards():
    return render_template("cards.html", items=session.get("items"), file_location=file_save_location)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("add.html")
    elif request.method == "POST":
        name = request.form["name"]
        primary_type = request.form["primary_type"]
        secondary_type = request.form.get("secondary_type", "")
        rarity = request.form["rarity"]
        uploaded_file = request.files.get("image")

        secondary_type = None if secondary_type == "" else secondary_type
        if primary_type == secondary_type:
            secondary_type = None

        if not all([name, primary_type, rarity, uploaded_file]):
            flash("All fields are required.", "danger")
            return redirect(url_for("add"))

        extension = os.path.splitext(uploaded_file.filename)[1].lower()
        if extension not in allowed_types:
            flash("Invalid file type. Only .png, .jpg, and .jpeg are allowed.", "danger")
            return redirect(url_for("add"))

        if uploaded_file.filename == "":
            flash("Please select a file to upload.", "danger")
            return redirect(url_for("add"))

        if uploaded_file.content_length > 16 * 1024 * 1024:
            flash("File is too large. Maximum size is 16MB.", "danger")
            return redirect(url_for("add"))

        unique_name = f"{uuid.uuid4().hex}{extension}"
        filename = os.path.join(file_save_location, unique_name)
        uploaded_file.save(filename)

        item_id = uuid.uuid4().hex
        session["items"][item_id] = {
            "name": name,
            "type1": primary_type,
            "type2": secondary_type,
            "rarity": rarity,
            "image": unique_name
        }
        flash("Card added successfully!", "success")
        return redirect(url_for("view_cards"))


@app.errorhandler(413)
def too_large():
    flash("File is too large. Maximum size is 16MB.", "danger")
    return redirect(url_for("add"))


@app.route("/delete/<item_id>", methods=["POST"])
def delete(item_id):
    items = session.get("items", {})
    if item_id in items:
        file_to_delete = os.path.join(file_save_location, items[item_id]["image"])
        if os.path.exists(file_to_delete):
            os.remove(file_to_delete)

        del items[item_id]
        flash("Card deleted successfully!", "success")
    else:
        flash("Card not found.", "danger")
    return redirect(url_for("view_cards"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
