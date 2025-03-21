from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "hello_class"

#videoGames = []

@app.route("/", methods=["GET"])
def index():
    if "videoGames" not in session:
        print("clearing games")
        session["videoGames"] = []

    print(session.get("videoGames"))
    return render_template("index.html",games=session.get("videoGames"))

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("add.html")
    elif request.method == "POST":
        if "videoGames" not in session:
            print("Clearing session data")
            session["videoGames"] = []
        title = request.form.get("title", "invalid")
        plat = request.form.get("plat", "invalid")
        year = request.form.get("year", "invalid")
        session["videoGames"].append({"title":title, "plat":plat, "year":year})
        print(session.get("videoGames"))
        session.modified = True
        return redirect("/")


