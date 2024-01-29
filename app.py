from flask import Flask,flash, render_template, request, redirect, url_for, session, jsonify, abort
import mysql.connector
import datetime
import random
from flask_login import LoginManager, login_required, current_user
import os

#socketio library 
from flask_socketio import SocketIO, emit, send, join_room, leave_room, close_room, rooms, disconnect
from decimal import Decimal
#personal info script (efficient than older one)
import info,function


'''
#new import might be migrate to other python file in future, (currently testing,rollback will be require if testing fail)
from cachetools import TTLCache
from flask import make_response

'''

app = Flask(__name__, template_folder='template')
app.secret_key = 'mysecretkey'

socketio = SocketIO(app)
#cache = TTLCache(maxsize=100, ttl=10)


# Default Database configuration #casino database
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
    result= info.get_status(username)
    if result=='active':
        return True;
    else:
        return render_template('login.html', error='Account has been banned!')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Query the database for the user
    cursor = mydb.cursor()

    # Check if the user exists and the password is correct
    if info.check_username(username) and info.check_password(username,password)==True:
        # Authentication successful, update last_login and set session
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if info.get_priv(username) != 'banker' and checkstatus(username)== True:
            sql = "UPDATE user SET last_login = %s WHERE username = %s"
            val = (now, username)
            cursor.execute(sql, val)
            mydb.commit()
            # Set session
            session['username'] = username
            session['priv'] = info.get_priv(username)
            session['background_image'] = random.choice(['j1.png', 'j2.png', 'j3.png'])
            return redirect(url_for('lobby'))
        elif info.get_priv(username) == 'banker' and checkstatus(username)== True:
            session['username'] = username
            session['priv'] = info.get_priv(username)
            session['background_image'] = random.choice(['banker.jpg'])
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
    
    result= info.check_password(username,password)
    # Check if the user exists and the password is correct
    if username is not None and result==True:
        return redirect(url_for("lobby", username=username))
    else:
        return render_template("login.html", error="Invalid username or password")

@socketio.on('update_balance')
def handle_update_balance(data):
    # Handle balance update logic here
    username = data['username']
    new_balance = info.get_balance(username)
    socketio.emit('balance_updated', {'balance': new_balance}, room=username)

@app.route('/lobby')
def lobby():
    # Get the user's current balance and privileges
    username = session.get('username')
    if username == None:
        return redirect(url_for("index"))
    background_image=session.get('background_image')
    socketio.emit('user_join', {'username': username}, room=username)
    priv= info.get_priv(username)
    # Determine whether to show the Win/Loss button based on user's privileges
    show_winloss = False
    if priv in ['banker', 'admin']:
        show_winloss = True
    # Render the lobby template with the appropriate parameters
    return render_template('lobby.html', balance= info.get_balance(username),username=username , priv=priv, show_winloss=show_winloss, background_image=background_image)


@app.route('/topup', methods=['GET', 'POST'])
def topup():
    from function import topup_function
    # Get the user's current balance and privileges
    username = session.get('username')
    priv = info.get_priv(username)
    background_image = session.get('background_image')

    if request.method == 'POST':
        if priv == 'admin':
            # Call the topup_function from function.py
            return topup_function(request, info.get_balance(username) , username, is_admin=True)
        else:
            # Call the topup_function from function.py
            return topup_function(request, info.get_balance(username) , username, is_admin=False)

    else:
        # Render the appropriate topup page based on the user's privileges
        if priv == 'admin':
            return render_template('topup_admin.html', balance=info.get_balance(username) , background_image=background_image)
        else:
            return render_template('topup.html', balance=info.get_balance(username) , is_admin=False, background_image=background_image)

@app.route('/logout')
def logout():
    # Update the last_logout field in the database
    now = info.get_now()
    username = session.get('username')
    info.update_logout(username,now)

    # Clear the session data and redirect to the index page
    session.pop('username', None)
    session.pop('balance', None)
    session.pop('background_image', None)
    return redirect(url_for('index'))

@app.route('/blackjack')
def blackjack():
    username = session.get('username')
    current_balance = info.get_balance(username)
    return render_template('blackjack.html', username=username,balance=current_balance, background_image=session.get('background_image'))
    


# Create an instance of the BlackjackGame class
from function import BlackjackGame

blackjack_game = BlackjackGame()


@app.route('/start_blackjack')
def start_blackjack():
    username = session.get('username')
    current_balance = info.get_balance(username)

    # If the game has not started, or the initial deal hasn't happened yet, render the initial state
    if not blackjack_game.game_state['game_started']:
        return render_template('blackjack.html', **blackjack_game.game_state, username=username, balance=current_balance)

    # Emit initial game state to the client
    emit('game_state', blackjack_game.game_state, namespace='/game')

    return render_template('blackjack.html', **blackjack_game.game_state, username=username, balance=current_balance)

# WebSocket event handlers
@socketio.on('start_game', namespace='/game')
def start_game():
    # Reset game state and start a new game
    blackjack_game.start_game()

    # Emit the initial game state to the client
    emit('game_state', blackjack_game.game_state, namespace='/game', broadcast=True)

@socketio.on('player_action', namespace='/game')
def player_action(data):
    action = data['action']
    blackjack_game.player_action(action)

    # Emit the updated game state to the client
    emit('game_state', blackjack_game.game_state, namespace='/game', broadcast=True)


PRIV_ADMIN = 'admin'
PRIV_BANKER = 'banker'

RESULT_WIN = 'win'
RESULT_LOSS = 'loss'

@app.route('/winloss', methods=['GET', 'POST'])
def winloss():
    priv = session.get('priv')
    if priv not in [PRIV_ADMIN, PRIV_BANKER]:
        abort(403)

    username = session.get('username')
    current_balance = info.get_balance(username)
    background_image = session.get('background_image')

    if request.method == 'POST':
        bet_amount = float(request.form['bet_amount'])

        if bet_amount > current_balance:
            flash('Bet amount cannot be greater than your current balance!', 'danger')
            return redirect(url_for('winloss'))

        if request.form['submit'] == 'win':
            handle_win(username, bet_amount)
            flash(('success', f'Successfully won ${bet_amount * 2}!'))
        elif request.form['submit'] == 'loss':
            handle_loss(username, bet_amount)
            flash(('warning', 'Better luck next time!'))

        return redirect(url_for('winloss'))

    return render_template('winloss.html', balance=info.get_balance(username), background_image=background_image)

#for win loss game (win)
def handle_win(username, bet_amount):
    new_balance = info.get_balance(username) + Decimal(str(bet_amount)) * 2
    info.update_balance(username, new_balance)
    info.update_balance(PRIV_BANKER, info.get_balance(PRIV_BANKER) - Decimal(str(bet_amount)) * 2)
    insert_winloss_record(username, bet_amount, RESULT_WIN)

#for win loss game (loss)
def handle_loss(username, bet_amount):
    new_balance = info.get_balance(username) - Decimal(str(bet_amount))
    info.update_balance(username, new_balance)
    info.update_balance(PRIV_BANKER, info.get_balance(PRIV_BANKER) + bet_amount)
    insert_winloss_record(username, bet_amount, RESULT_LOSS)


def insert_winloss_record(username, bet_amount, result):
    cursor = mydb.cursor()
    cursor.execute(
        'INSERT INTO winloss_history (username, bet_amount, result, createtime) VALUES (%s, %s, %s, %s)',
        (username, bet_amount, result, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    )
    mydb.commit()
    cursor.close()

@app.route('/slotmachine')
def slotmachine():
    # Get the user's current balance and privileges
    username = session.get('username')
    # Check if the user exists

    current_balance = info.get_balance(username)
    if current_balance is None:
        flash('User not found!', 'danger')
        return redirect(url_for('login'))
    # Initialize symbols to an empty list
    symbols = []
    # Render the slot machine template with the appropriate parameters
    return render_template('slotmachine.html', username=username, balance=info.get_balance(username) , symbols=symbols, background_image=session.get('background_image'))

@app.route('/spin', methods=['POST'])
def spin():
    from function import spin_slot_machine
    username = session.get('username')
    bet_amount = float(request.form['bet_amount'])

    symbols, bet_amount, winnings, session['balance'] = spin_slot_machine(username, bet_amount)

    flash(f'{symbols[0]}, {symbols[1]}, {symbols[2]}')
    current_balance = info.get_balance(username)
    return render_template('slotmachine_results.html', username=username, symbols=symbols, bet_amount=bet_amount,
                           winnings=winnings, balance=current_balance)

@app.errorhandler(405)
@app.errorhandler(404)
def error_handler(error):
    
    random_image = function.errorleh()
    if 'username' in session:
        return render_template('404.html', random_image=random_image, home_url=url_for('lobby'))
    else:
        return render_template('404.html', random_image=random_image, home_url=url_for('index'))


@app.route('/referal', methods=['GET', 'POST'])
def referal():
    
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

    return render_template('referal.html',background_image=session.get('background_image'),balance=info.get_balance(username))

@app.route('/viewref')
def view_referrals():
    
    referrals = function.get_referrals()
    return render_template('viewref.html', referrals=referrals, background_image=session.get('background_image'),balance=info.get_balance(session.get('username')))

@app.route('/referalcollect', methods=['GET', 'POST'])
def referalcollect():
    return render_template('referalcollect.html', background_image=session.get('background_image'), balance=info.get_balance(session.get('username')))

@app.route('/referalcollectsubmit', methods=['GET', 'POST'])
def refsubmit():
    
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
    function.delete_referral(referral_id)
    flash('Referral deleted successfully', 'success')
    return redirect(url_for('view_referrals'))

@app.route('/delete_all_referrals', methods=['POST'])
def delete_all_referrals():
    function.delete_all_referrals()
    flash('All referrals deleted successfully', 'success')
    return redirect(url_for('view_referrals'))

@app.route('/game4d')
def game4d():
    username = session.get('username')
    return render_template('game4d.html',background_image=session.get('background_image'), balance=info.get_balance(username))


#admin 4d game control page
@app.route('/game4dadmin')
def admin4dsubmit():
    username = session.get('username')
    return render_template('game4dadmin.html',background_image=session.get('background_image'), balance=info.get_balance(username))



# This is the user to submit the 4d
@app.route('/submit4dtoto', methods=['POST'])
def submit_4d():
    username = session.get('username')
    toto_number = request.form.get('4d_number')  # Corrected input name
    cursor = mydb.cursor()
    cursor.execute('INSERT INTO toto_4d (toto_number, username) VALUES (%s, %s)', (toto_number, username))
    mydb.commit()
    cursor.close()
    return redirect(url_for('lobby'))


@app.route('/admintoto')
def admintoto():
    username = session.get('username')
    balace = info.get_balance(username)
    return render_template('admintoto.html',background_image=session.get('background_image'), balance=info.get_balance(username))

#toto game (update require)
@app.route('/admintotosubmit', methods=['POST'])
def admin4dtotosubmit():
    username = session.get('username')
    group1 = request.form.get('group1')
    group2 = request.form.get('group2')
    group3 = request.form.get('group3')
    group4 = request.form.get('group4')
    group5 = request.form.get('group5')
    group6 = request.form.get('group6')
    group7 = request.form.get('group7')
    cursor = mydb.cursor()
    #cursor.execute('INSERT INTO toto_4d (toto_number, username) VALUES (%s, %s)', (toto_number, username))
    mydb.commit()
    cursor.close()
    return redirect(url_for('lobby'))


if __name__ == '__main__':
    app.run(debug=True)