from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/submit", methods=["POST"])
def submit():
    username = request.form.get("username")
    password = request.form.get("password")
    # Add your authentication logic here
    # If the login is successful, redirect the user to the lobby page
    if username == "admin" and password == "password":
        return redirect(url_for("lobby", username=username))
    else:
        return render_template("login.html", error="Invalid username or password")

@app.route("/lobby/<username>")
def lobby(username):
    return render_template("lobby.html", username=username)

@app.route("/blackjack")
def blackjack():
    # Add your blackjack logic here
    return "Blackjack game page"

if __name__ == "__main__":
    app.run(debug=True)