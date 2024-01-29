import random
import mysql.connector
import string
import datetime
from flask import Flask,flash, render_template, request, redirect, url_for, session, jsonify, abort
import info 

rdb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="casino_regis")

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


    new_balance = info.get_balance(username) + balance
    info.update_balance(username, new_balance)  

    rdb.commit()
    return new_balance


def errorleh():
	random_image = random.choice(ERROR_IMAGES)
	return random_image


def spin_slot_machine(username, bet_amount):

    current_balance = info.get_balance(username)


    if bet_amount > current_balance:
        flash('Bet amount cannot be greater than your current balance!', 'danger')
        return redirect(url_for('slotmachine'))

    new_balance = current_balance - bet_amount
    info.update_balance(username, new_balance)

    banker_balance = info.get_balance('banker') + bet_amount
    info.update_balance('banker', banker_balance)

    symbols = []
    for _ in range(3):
        symbols.append(random.choice(['chicken', 'cow', 'dog', 'dragon', 'goat', 'monkey', 'pig', 'rabbit', 'rat',
                                      'snake', 'tiger', 'horse']))

    # checking the function all work for not
    symbols[0] = symbols[1] = symbols[2] = 'dragon'
    winnings = 0
    symbol_winnings = {
        "chicken": 10,
        "cow": 10,
        "dog": 10,
        "dragon": 20,
        "goat": 10,
        "monkey": 10,
        "pig": 10,
        "rabbit": 10,
        "rat": 10,
        "snake": 10,
        "tiger": 10,
        "horse": 10
    }

    if symbols[0] == symbols[1] == symbols[2]:
        if symbols[0] in symbol_winnings:
            winnings = bet_amount * symbol_winnings[symbols[0]]

    if winnings > 0:
        banker_balance -= winnings
        new_balance += winnings
        info.update_balance('banker', banker_balance)
        info.update_balance(username, new_balance)
    info.insert_slotmachine(username, bet_amount, ','.join(symbols), winnings)

    return symbols, bet_amount, winnings, new_balance

def topup_function(request, current_balance, username, is_admin=False):
    if is_admin:
        # Get the amount and helper username to top up from the form
        amount = int(request.form['amount'])
        helper_username = request.form['helper_username']

        # Get the helper's current balance
        helper_balance = info.get_balance(helper_username)

        # Top up the helper's balance
        new_helper_balance = helper_balance + amount
        # Insert a new row into the topup_history table
        bef_topup = helper_balance
        after_topup = new_helper_balance
        topup_amt = amount
        info.insert_topup(helper_username, bef_topup, after_topup, topup_amt, username)

        # Everything is recorded already, then it will update the real balance, otherwise the record is just a record, not an actual balance effect
        info.update_balance(helper_username, new_helper_balance)

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
        info.update_balance(username, new_balance)

        # Insert a new row into the topup_history table
        bef_topup = current_balance
        after_topup = current_balance + amount
        topup_amt = amount
        info.insert_topup(username, bef_topup, after_topup, topup_amt, username)

        # After all the records have been inserted, the balance will be updated
        new_balance = current_balance + amount
        info.update_balance(username, new_balance)  

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

cards = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}

# Function to shuffle a deck of cards
def create_deck():
    deck = list(cards.keys()) * 4  # Four suits
    random.shuffle(deck)
    return deck

def create_deck_emoji():
    deck = list(cards.keys()) * 4  # Four suits
    deck_with_emoji = ['♠️ ' + card for card in deck if card != 'A']
    deck_with_emoji += ['♠️ A'] * deck.count('A')
    deck_with_emoji += ['♥️ ' + card for card in deck if card != 'A']
    deck_with_emoji += ['♥️ A'] * deck.count('A')
    deck_with_emoji += ['♦️ ' + card for card in deck if card != 'A']
    deck_with_emoji += ['♦️ A'] * deck.count('A')
    deck_with_emoji += ['♣️ ' + card for card in deck if card != 'A']
    deck_with_emoji += ['♣️ A'] * deck.count('A')
    random.shuffle(deck_with_emoji)
    return deck_with_emoji

# Function to calculate the total value of a hand
def calculate_hand(hand):
    total = sum([cards[card] for card in hand])
    # Handle Aces (count as 11 or 1)
    aces = hand.count('A')
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total

# Function to calculate the total value of a hand with emoji deck
def calculate_hand_emoji(hand):
    total = sum([cards[card[3:]] for card in hand])
    # Handle Aces (count as 11 or 1)
    aces = hand.count('A')
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total

#this is the blackjack game that for one single player
class BlackjackGame:
    def __init__(self):
        self.game_state = {
            'dealer_hand': [],
            'player_hand': [],
            'dealer_score': 0,
            'player_score': 0,
            'outcome': "",
            'game_started': False
        }
        self.deck = []

    def reset_game_state(self):
        self.deck = []
        self.game_state = {
            'dealer_hand': [],
            'player_hand': [],
            'dealer_score': 0,
            'player_score': 0,
            'outcome': "",
            'game_started': False
        }

    def start_game(self):
        self.reset_game_state()
        self.deck = create_deck_emoji()
        self.game_state['dealer_hand'] = [self.deck.pop(), self.deck.pop()]
        self.game_state['player_hand'] = [self.deck.pop(), self.deck.pop()]
        self.game_state['dealer_score'] = calculate_hand_emoji(self.game_state['dealer_hand'])
        self.game_state['player_score'] = calculate_hand_emoji(self.game_state['player_hand'])
        self.game_state['outcome'] = ""
        self.game_state['game_started'] = True

    def player_action(self, action):
        if self.game_state['game_started']:
            if action == 'hit':
                self.game_state['player_hand'].append(self.deck.pop())
                self.game_state['player_score'] = calculate_hand_emoji(self.game_state['player_hand'])
                if self.game_state['player_score'] > 21:
                    self.game_state['outcome'] = 'You have busted! You Lose!'
                    self.game_state['game_started'] = False  # End the game

            elif action == 'stand':
                print('Player stands. Dealer is playing.')

                # After player action, dealer will act
                while self.game_state['dealer_score'] < 17:
                    self.game_state['dealer_hand'].append(self.deck.pop())
                    self.game_state['dealer_score'] = calculate_hand_emoji(self.game_state['dealer_hand'])

                # Final calculate here
                self.determine_outcome()
                self.game_state['game_started'] = False  # End the game

    def determine_outcome(self):
        if self.game_state['player_score'] > 21:
            self.game_state['outcome'] = 'Player Busts. Dealer Wins!'
        elif self.game_state['dealer_score'] > 21 or self.game_state['dealer_score'] < self.game_state['player_score']:
            self.game_state['outcome'] = 'Player Wins!'
        elif self.game_state['dealer_score'] > self.game_state['player_score']:
            self.game_state['outcome'] = 'Dealer Wins!'
        elif self.game_state['dealer_score'] == self.game_state['player_score']:
            self.game_state['outcome'] = 'It\'s a Tie!'
        else:
            self.game_state['outcome'] = 'Error, Please check with the Dealer!'