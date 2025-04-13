from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_session import Session
import uuid
import csv
import os

app = Flask(__name__)
app.secret_key = "password"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

csv_file = "static/items.csv"
file_save_location = "static/images"
allowed_types = [".png", ".jpg", ".jpeg"]

os.makedirs(file_save_location, exist_ok=True)

@app.before_request
def session_id():
    if "sid" not in session:
        session["sid"] = str(uuid.uuid4())
    if "items" not in session:
        session["items"] = load_items()

def load_items():
    items = {}
    if os.path.exists(csv_file):
        with open(csv_file, newline="")as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                item_id = row[0]
                sid = row[1]
                name = row[2]
                item_type = row[3]
                rarity = row[4]
                image = row[5]
                if sid == session["sid"]:
                    items[item_id] = {
                        "name": name,
                        "type": item_type,
                        "rarity": rarity,
                        "image": image
                    }
    return items

def save_items():
    with open(csv_file, "w", newline="")as file:
        writer = csv.writer(file)
        writer.writerow(["id", "sid", "Item name", "Item type", "Item Rarity", "Item image"])
        for item_id, item in session["items"].items():
            writer.writerow([item_id, session["sid"], item["name"], item["type"], item["rarity"], item["image"]])

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html",items=session.get("items"), file_location=file_save_location)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("add.html")
    elif request.method == "POST":
        item_name = request.form["name"]
        item_type = request.form["type"]
        item_rarity = request.form["rarity"]
        uploaded_file = request.files["image"]

        if uploaded_file.filename == "":
            flash("No file selected. Please upload an image.", "danger")
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
            "name": item_name,
            "type": item_type,
            "rarity": item_rarity,
            "image": unique_name
        }

        save_items()
        flash("Item added successfully!", "success")
        return redirect(url_for("index"))

if __name__ == "__main__":
   app.run(debug=True, host="0.0.0.0")


