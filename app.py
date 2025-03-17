from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/greet", methods=["POST"])
def greet():
    card = request.form.get("creditcard", "invalid")
    return render_template("greet.html", card=card)
