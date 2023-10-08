from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/login')
def login():
    # ...
    if authenticated:
        return redirect(url_for('lobby', username=username))
    else:
        return render_template('login.html', error='Invalid credentials')

@app.route('/lobby/<username>')
def lobby(username):
    # ...
    return render_template('lobby.html', username=username)