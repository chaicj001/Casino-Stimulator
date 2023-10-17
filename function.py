import random
import mysql.connector
import string
import datetime
from flask import Flask,flash, render_template, request, redirect, url_for, session, jsonify, abort
import rsa

rdb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="casino_regis")

mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="casino")

game4ddb= mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="game4d")

ERROR_IMAGES = [
    "https://media.giphy.com/media/hLwSzlKN8Fi6I/giphy.gif",
    "https://media.giphy.com/media/YyKPbc5OOTSQE/giphy.gif",
    "https://media1.giphy.com/media/TqiwHbFBaZ4ti/giphy.gif"
]

def create_referal():
    length = 10
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


def create_amount(balance_type):
    if balance_type == "low":
        amount = random.randint(2000, 5000)
    elif balance_type == "mid":
        amount = random.randint(5000, 10000)
    elif balance_type == "high":
        amount = random.randint(10000, 25000)
    elif balance_type == "vip":
        amount = 50000
    elif balance_type == "vvip":
        amount = 100000
    elif balance_type == "banker":
        amount = 1000000
    else:
        amount = 0  # Default value if balance_type is invalid
    return amount


def insertreftable(referral_code, balance_type,created):
    if balance_type == "banker":
        user_priv = "banker"
    else:
        user_priv = "user"
    amount = create_amount(balance_type)
    cursor = rdb.cursor()
    cursor.execute('INSERT INTO referal (referal_code, balance, user_priv,created_by) VALUES (%s, %s, %s, %s)',
                   (referral_code, amount, user_priv,created))
    rdb.commit()

def insertreftable2(referral_code, balance,created):
    cursor = rdb.cursor()
    cursor.execute('INSERT INTO referal (referal_code, balance, created) VALUES (%s, %s, %s)',
                   (referral_code, balance, created))
    rdb.commit()

def receivedref(referral, username):
    cursor = rdb.cursor()
    cursor.execute('SELECT balance, created_by FROM referal WHERE referal_code = %s', (referral,))
    result = cursor.fetchone()
    if result is None:
        abort(404)  # Redirect to a 404 error page

    balance = float(result[0])
    created = result[1]
    cursor.execute('INSERT INTO referal_tran (referal_code, balance, user_from, user_to) VALUES (%s, %s, %s, %s)',
                   (referral, balance, created, username))
    cursor.execute('DELETE FROM referal WHERE referal_code = %s', (referral,))

    cursor = mydb.cursor()
    cursor.execute('SELECT balance FROM user WHERE username = %s', (username,))
    result2 = cursor.fetchone()
    user_balance = float(result2[0])

    new_balance = user_balance + balance
    cursor.execute('UPDATE user SET balance = %s WHERE username = %s', (new_balance, username))

    mydb.commit()
    rdb.commit()
    return new_balance


def errorleh():
	random_image = random.choice(ERROR_IMAGES)
	return random_image


def spin_slot_machine(username, bet_amount):
    cursor = mydb.cursor()
    cursor.execute('SELECT balance, priv FROM user WHERE username = %s', (username,))
    result = cursor.fetchone()
    session['balance'] =current_balance = float(result[0])

    priv = result[1] if result else None

    if bet_amount > current_balance:
        flash('Bet amount cannot be greater than your current balance!', 'danger')
        return redirect(url_for('slotmachine'))

    session['balance'] =new_balance = current_balance - bet_amount
    cursor.execute('UPDATE user SET balance = %s WHERE username = %s', (new_balance, username))
    cursor.execute('SELECT balance FROM user WHERE username = %s', ('banker',))
    banker_result = cursor.fetchone()
    banker_balance = float(banker_result[0]) + bet_amount
    cursor.execute('UPDATE user SET balance = %s WHERE username = %s', (banker_balance, 'banker'))

    symbols = []
    for _ in range(3):
        symbols.append(random.choice(['chicken', 'cow', 'dog', 'dragon', 'goat', 'monkey', 'pig', 'rabbit', 'rat',
                                      'snake', 'tiger', 'horse']))

    symbols[0] = symbols[1] = symbols[2] = 'dragon'
    winnings = 0
    if symbols[0] == symbols[1] == symbols[2]:
        if symbols[0] == "chicken":
            winnings = bet_amount * 10
        elif symbols[0] == "cow":
            winnings = bet_amount * 10
        elif symbols[0] == "dog":
            winnings = bet_amount * 10
        elif symbols[0] == "dragon":
            winnings = bet_amount * 20
        elif symbols[0] == "goat":
            winnings = bet_amount * 10
        elif symbols[0] == "monkey":
            winnings = bet_amount * 10
        elif symbols[0] == "pig":
            winnings = bet_amount * 10
        elif symbols[0] == "rabbit":
            winnings = bet_amount * 10
        elif symbols[0] == "rat":
            winnings = bet_amount * 10
        elif symbols[0] == "snake":
            winnings = bet_amount * 10
        elif symbols[0] == "tiger":
            winnings = bet_amount * 10
        elif symbols[0] == "horse":
            winnings = bet_amount * 10

    if winnings > 0:
        banker_balance -= winnings
        new_balance += winnings
        session['balance'] = new_balance
        cursor.execute('UPDATE user SET balance = %s WHERE username = "banker"', (banker_balance,))
        mydb.commit()
        cursor.execute('UPDATE user SET balance = %s WHERE username = %s', (new_balance, username))
        mydb.commit()

    cursor.execute(
        'INSERT INTO slot_machine_history (username, bet_amount, winnings, symbols, spin_time) VALUES (%s, %s, %s, %s, %s)',
        (username, bet_amount, winnings, ','.join(symbols), datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    mydb.commit()
    cursor.close()

    return symbols, bet_amount, winnings, new_balance

def topup_function(request, cursor, current_balance, username, background_image, is_admin=False):
    if is_admin:
        # Get the amount and helper username to top up from the form
        amount = int(request.form['amount'])
        helper_username = request.form['helper_username']

        # Get the helper's current balance
        cursor.execute('SELECT balance FROM user WHERE username = %s', (helper_username,))
        helper_balance = float(cursor.fetchone()[0])

        # Top up the helper's balance
        new_helper_balance = helper_balance + amount
        # Insert a new row into the topup_history table
        bef_topup = helper_balance
        after_topup = new_helper_balance
        topup_amt = amount
        topup_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('INSERT INTO topup_history (username, bef_topup, after_topup, topup_amt, topup_time, user_topup) VALUES (%s, %s, %s, %s, %s, %s)',
                       (helper_username, bef_topup, after_topup, topup_amt, topup_time, username))

        # Select the topup id first since it is the trigger
        cursor.execute('SELECT topup_id from topup_history WHERE username=%s AND topup_amt= %s AND topup_time= %s',
                       (helper_username, topup_amt, topup_time,))
        secondid = cursor.fetchone()[0]
        cursor.execute('INSERT INTO transaction(transaction_id2,user,amt_bef_transaction,amt_aft_transaction,total_amt_transaction, transaction_comment)VALUES(%s,%s,%s,%s,%s,%s)',
                       (secondid, helper_username, bef_topup, after_topup, topup_amt, 'admin page topup'))

        # Everything is recorded already, then it will update the real balance, otherwise the record is just a record, not an actual balance effect
        cursor.execute('UPDATE user SET balance = %s WHERE username = %s', (new_helper_balance, helper_username))

        # Close the database connection
        mydb.commit()
        cursor.close()

        # Redirect back to the lobby page with a success message
        flash(f'Successfully topped up ${amount} for {helper_username}', 'success')
        return redirect(url_for('lobby'))
    else:
        # Get the amount to top up from the form
        amount = int(request.form['amount'])

        # Limit normal users to top up $10,000
        if amount > 10000:
            flash('Top-up amount exceeds limit', 'danger')
            return redirect(url_for('topup'))

        # Update the balance in the database
        new_balance = current_balance + amount
        cursor.execute('UPDATE user SET balance = %s WHERE username = %s', (new_balance, username))

        # Insert a new row into the topup_history table
        bef_topup = current_balance
        after_topup = current_balance + amount
        topup_amt = amount
        topup_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('INSERT INTO topup_history (username, bef_topup, after_topup, topup_amt, topup_time) VALUES (%s, %s, %s, %s, %s)',
                       (username, bef_topup, after_topup, topup_amt, topup_time))

        # Insert a new row into the transaction table
        cursor.execute('SELECT topup_id from topup_history WHERE username=%s AND topup_amt= %s AND topup_time= %s',
                       (username, topup_amt, topup_time,))
        transaction_id2 = cursor.fetchone()[0]
        transaction_comment = 'user topup'
        cursor.execute('INSERT INTO transaction (transaction_id2, user, amt_bef_transaction, amt_aft_transaction, total_amt_transaction, transaction_comment) VALUES (%s, %s, %s, %s, %s, %s)',
                       (transaction_id2, username, bef_topup, after_topup, topup_amt, transaction_comment))

        # After all the records have been inserted, the balance will be updated
        new_balance = current_balance + amount
        cursor.execute('UPDATE user SET balance = %s WHERE username = %s', (new_balance, username))

        # Close the database connection
        mydb.commit()
        cursor.close()

        # Redirect back to the lobby page with a success message
        flash(f'Successfully topped up ${amount}', 'success')
        return redirect(url_for('lobby'))


def get_referrals():
    # Implement the logic to fetch referrals from the database
    cursor = rdb.cursor()
    query = "SELECT * FROM referal"
    cursor.execute(query)
    referrals = cursor.fetchall()
    return referrals

def delete_referral(referral_code):
    cursor = rdb.cursor()
    query = "DELETE FROM referal WHERE referal_code = %s"
    cursor.execute(query, (referral_code,))
    rdb.commit()

def delete_all_referrals():
    # Implement the logic to delete all referral codes from the database
    cursor = rdb.cursor()
    cursor.execute('DELETE FROM referal')
    rdb.commit()

