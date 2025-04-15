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
    if "sid" not in session:
        session["sid"] = str(uuid.uuid4())
    if "items" not in session:
        session["items"] = {}

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
        name = request.form.get("name", "invalid")
        pokemon_type = request.form.get("type", "invalid")
        rarity = request.form.get("rarity", "invalid")
        uploaded_file = request.files.get("image")

        if not name or not pokemon_type or not rarity or not uploaded_file:
            flash("All fields are required.", "danger")
            return redirect(url_for("add"))

        extension = os.path.splitext(uploaded_file.filename)[1]
        if extension not in allowed_types:
            flash("Invalid file type. Only .png, .jpg, and .jpeg are allowed.", "danger")
            return redirect(url_for("add"))

        unique_name = f"{uuid.uuid4().hex}{extension}"
        filename = os.path.join(file_save_location, unique_name)
        uploaded_file.save(filename)

        item_id = uuid.uuid4().hex
        session["items"][item_id] = {
            "name": name,
            "type": pokemon_type,
            "rarity": rarity,
            "image": unique_name
        }
        session.modified = True
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
        del items[item_id]
        session["items"] = items
        session.modified = True
        flash("Card deleted successfully!", "success")
    else:
        flash("Card not found.", "danger")
    return redirect(url_for("view_cards"))

if __name__ == "__main__":
   app.run(debug=True, host="0.0.0.0")