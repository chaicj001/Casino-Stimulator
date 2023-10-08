from flask import Flask,flash, render_template, request, redirect, url_for, session, jsonify, abort
import mysql.connector
import datetime
import random
from flask_login import LoginManager, login_required, current_user
import os

app = Flask(__name__, template_folder='template')
app.secret_key = 'mysecretkey'

# Database configuration
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="casino"
)


@app.route('/')
def index():
    return render_template('login.html')

def checkstatus(username):
    cursor = mydb.cursor()
    query = "SELECT status FROM user WHERE username = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    if user[0]=='active':
        return True;
    else:
        return render_template('login.html', error='Account has been banned!')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Query the database for the user
    cursor = mydb.cursor()
    query = "SELECT * FROM user WHERE username = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()

    # Check if the user exists and the password is correct
    if user is not None and user[1] == password:
        # Authentication successful, update last_login and set session
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if user[2] != 'banker' and checkstatus(username)== True:
            sql = "UPDATE user SET last_login = %s WHERE username = %s"
            val = (now, username)
            cursor.execute(sql, val)
            mydb.commit()
            # Set session
            session['username'] = username
            session['priv'] = user[2]
            session['background_image'] = random.choice(['j1.png', 'j2.png', 'j3.png'])
            return redirect(url_for('lobby'))
        elif user[2] == 'banker' and checkstatus(username)== True:
            session['username'] = username
            session['priv'] = user[2]
            session['background_image'] = random.choice(['j1.png', 'j2.png', 'j3.png'])
            return redirect(url_for('lobby'))
        else:
            return render_template('login.html', error='Account has a problem')
    else:
        # Authentication failed, return an error message to the user
        return render_template('login.html', error='Invalid username or password')



@app.route("/submit", methods=["POST"])
def submit():
    username = request.form.get("username")
    password = request.form.get("password")
    
    # Query the database for the user
    cursor = mydb.cursor()
    query = "SELECT * FROM user WHERE username = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()

    # Check if the user exists and the password is correct
    if user is not None and user[1] == password:
        return redirect(url_for("lobby", username=username))
    else:
        return render_template("login.html", error="Invalid username or password")

@app.route('/lobby')
def lobby():
    # Get the user's current balance and privileges
    username = session.get('username')
    cursor = mydb.cursor()
    cursor.execute('SELECT balance, priv FROM user WHERE username = %s', (username,))
    result = cursor.fetchone()
    session['balance'] = float(result[0])
    priv = result[1] if result else None
    print(priv)  # Add this line to check the value of priv

    # Determine whether to show the Win/Loss button based on user's privileges
    show_winloss = False
    if priv in ['banker', 'admin']:
        show_winloss = True

    # Randomly choose a background image from j1, j2, j3
    background_image=session.get('background_image')
    # Render the lobby template with the appropriate parameters
    return render_template('lobby.html', username=username, balance=session['balance'] , priv=priv, show_winloss=show_winloss, background_image=background_image)


@app.route('/topup', methods=['GET', 'POST'])
def topup():
    from function import topup_function
    # Get the user's current balance and privileges
    username = session.get('username')
    cursor = mydb.cursor()
    cursor.execute('SELECT balance, priv FROM user WHERE username = %s', (username,))
    result = cursor.fetchone()
    session['balance']  = float(result[0])
    priv = result[1]
    background_image = session.get('background_image')

    if request.method == 'POST':
        if priv == 'admin':
            # Call the topup_function from function.py
            return topup_function(request, cursor, session['balance'] , username, background_image, is_admin=True)
        else:
            # Call the topup_function from function.py
            return topup_function(request, cursor, session['balance'] , username, background_image, is_admin=False)

    else:
        # Render the appropriate topup page based on the user's privileges
        if priv == 'admin':
            return render_template('topup_admin.html', balance=session['balance'] , background_image=background_image)
        else:
            return render_template('topup.html', balance=session['balance'] , is_admin=False, background_image=background_image)

@app.route('/logout')
def logout():
    # Update the last_logout field in the database
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    username = session.get('username')
    cursor = mydb.cursor()
    cursor.execute("UPDATE user SET last_logout = %s WHERE username = %s", (now, username))
    mydb.commit()
    cursor.close()

    # Clear the session data and redirect to the index page
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/blackjack')
def blackjack():
    username = session.get('username')
    cursor = mydb.cursor()
    cursor.execute('SELECT balance FROM user WHERE username = %s', (username,))
    current_balance = float(cursor.fetchone()[0])

    return render_template('blackjack.html',balance=current_balance)

@app.route('/winloss', methods=['GET', 'POST'])
def winloss():
    # Check if the user has admin or banker privileges
    priv = session.get('priv')
    if priv != 'admin' and priv != 'banker':
        abort(403) # Return a 403 Forbidden error if the user does not have the required privileges

    # Get the user's current balance
    username = session.get('username')
    cursor = mydb.cursor()
    cursor.execute('SELECT balance FROM user WHERE username = %s', (username,))
    session['balance'] = current_balance = float(cursor.fetchone()[0])
    background_image=session.get('background_image')

    if request.method == 'POST':
        # Get the bet amount from the form
        bet_amount = float(request.form['bet_amount'])

        # Check if the bet amount is greater than the user's current balance
        if bet_amount > current_balance:
            flash('Bet amount cannot be greater than your current balance!', 'danger')
            return redirect(url_for('winloss'))

        if request.form['submit'] == 'win':
            # Double the bet amount and add it to the user's balance
            new_balance = current_balance + bet_amount * 2
            cursor.execute('UPDATE user SET balance = %s WHERE username = %s', (new_balance, username))

            # Deduct double the bet amount from the banker's balance
            cursor.execute('UPDATE user SET balance = balance - %s WHERE priv = %s', (bet_amount * 2, 'banker'))

            # Insert a record into the winloss_history table
            cursor.execute('INSERT INTO winloss_history (username, bet_amount, result, createtime) VALUES (%s, %s, %s, %s)', (username, bet_amount, 'win', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

            # Commit the changes to the database and close the cursor
            mydb.commit()
            cursor.close()

            # Redirect back to the winloss page with a success message
            flash(('success', f'Successfully won ${bet_amount * 2}!'))
            return redirect(url_for('winloss'))
        elif request.form['submit'] == 'loss':
            # Subtract the bet amount from the user's balance
            new_balance = current_balance - bet_amount
            cursor.execute('UPDATE user SET balance = %s WHERE username = %s', (new_balance, username))

            # Add the bet amount to the banker's balance
            cursor.execute('UPDATE user SET balance = balance + %s WHERE priv = %s', (bet_amount, 'banker'))

            # Insert a record into the winloss_history table
            cursor.execute('INSERT INTO winloss_history (username, bet_amount, result, createtime) VALUES (%s, %s, %s, %s)', (username, bet_amount, 'loss', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

            # Commit the changes to the database and close the cursor
            mydb.commit()
            cursor.close()

            # Redirect back to the winloss page with a success message
            flash(('warning', 'Better luck next time!'))
            return redirect(url_for('winloss'))

    else:
        # Render the winloss page template with the current balance
        return render_template('winloss.html', balance=current_balance,background_image=background_image)

@app.route('/slotmachine')
def slotmachine():
    # Get the user's current balance and privileges
    username = session.get('username')
    cursor = mydb.cursor()
    cursor.execute('SELECT balance, priv FROM user WHERE username = %s', (username,))
    result = cursor.fetchone()
    # Check if the user exists
    if result is None:
        flash('User not found!', 'danger')
        return redirect(url_for('login'))
    balance = float(result[0])
    priv = result[1]

    # Initialize symbols to an empty list
    symbols = []

    # Render the slot machine template with the appropriate parameters
    return render_template('slotmachine.html', username=username, balance=balance, symbols=symbols)

@app.route('/spin', methods=['POST'])
def spin():
    from function import spin_slot_machine
    username = session.get('username')
    bet_amount = float(request.form['bet_amount'])

    symbols, bet_amount, winnings, session['balance'] = spin_slot_machine(username, bet_amount)

    flash(f'{symbols[0]}, {symbols[1]}, {symbols[2]}')
    cursor = mydb.cursor()
    cursor.execute('SELECT balance, priv FROM user WHERE username = %s', (username,))
    result = cursor.fetchone()
    current_balance = float(result[0])
    return render_template('slotmachine_results.html', username=username, symbols=symbols, bet_amount=bet_amount,
                           winnings=winnings, balance=current_balance)

@app.errorhandler(405)
@app.errorhandler(404)
def error_handler(error):
    import function
    random_image = function.errorleh()
    if 'username' in session:
        return render_template('404.html', random_image=random_image, home_url=url_for('lobby'))
    else:
        return render_template('404.html', random_image=random_image, home_url=url_for('index'))


@app.route('/referal', methods=['GET', 'POST'])
def referal():
    import function
    username = session.get('username')
    if 'username' not in session:
        return redirect(url_for('index'))  # Redirect to login page or display an error message

    balance_type = None  # Initialize balance_type
    if request.method == 'POST':
        balance_type = request.form['balance-type']
        if 'generate_single' in request.form:
            referral_code = function.create_referal()
            # Insert the referral code into the database with the balance type
            function.insertreftable(referral_code, balance_type,username)
            flash(f"Generated referral code: {referral_code}")
        elif 'generate_multiple' in request.form:
            num_referrals = 5 if request.form['generate_multiple'] == 'Generate Multiple (5)' else 10
            referral_codes = [function.create_referal() for _ in range(num_referrals)]
            # Insert the referral codes into the database with the balance type
            for referral_code in referral_codes:
                function.insertreftable(referral_code, balance_type,username)
            flash(f"Generated {num_referrals} referral codes: {', '.join(referral_codes)}")

    return render_template('referal.html',background_image=session.get('background_image'),balance=session.get('balance'))

@app.route('/viewref')
def view_referrals():
    import function
    referrals = function.get_referrals()
    return render_template('viewref.html', referrals=referrals, background_image=session.get('background_image'),balance=session.get('balance'))

@app.route('/referalcollect', methods=['GET', 'POST'])
def referalcollect():
    return render_template('referalcollect.html', background_image=session.get('background_image'), balance=session.get('balance'))

@app.route('/referalcollectsubmit', methods=['GET', 'POST'])
def refsubmit():
    import function
    if request.method == 'POST':
        referral_code = request.form['referralCode']
        username = session.get('username')

        # Call the function to process the referral and update user balances
        balance= function.receivedref(referral_code, username)
        # Redirect to the lobby after processing the referral
        return redirect('/lobby')
    else:
        return redirect('/lobby')


@app.route('/delete_referral/<referral_id>', methods=['POST'])
def delete_referral(referral_id):
    import function
    function.delete_referral(referral_id)
    flash('Referral deleted successfully', 'success')
    return redirect(url_for('view_referrals'))

@app.route('/delete_all_referrals', methods=['POST'])
def delete_all_referrals():
    import function
    function.delete_all_referrals()
    flash('All referrals deleted successfully', 'success')
    return redirect(url_for('view_referrals'))

@app.route('/toto', methods=['POST'])
def toto():
    username = session.get('username')
    cursor = mydb.cursor()
    cursor.execute('SELECT balance FROM user WHERE username = %s', (username,))
    balance = float(cursor.fetchone()[0])
    return redirect(url_for('toto'))
   # return render_template('toto.html', background_image=session.get('background_image'), balance=balance)















if __name__ == '__main__':
    app.run(debug=True)