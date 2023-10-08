import random
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/play_blackjack')
def play_blackjack():
    # Set up the deck of cards
    deck = [2,3,4,5,6,7,8,9,10,'J','Q','K','A'] * 4

    # Shuffle the deck
    random.shuffle(deck)

    # Deal the cards
    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]

    # Keep track of the scores
    player_score = sum(get_card_value(card) for card in player_hand)
    dealer_score = sum(get_card_value(card) for card in dealer_hand)

    # Player's turn
    while player_score < 21:
        choice = input(f"Your hand: {player_hand} ({player_score}). Hit or stand? ").lower()
        if choice == "hit":
            player_hand.append(deck.pop())
            player_score = sum(get_card_value(card) for card in player_hand)
        elif choice == "stand":
            break

    if player_score > 21:
        return jsonify({'result': "Bust! You lose."})

    # Dealer's turn
    while dealer_score < 17:
        dealer_hand.append(deck.pop())
        dealer_score = sum(get_card_value(card) for card in dealer_hand)

    # Determine the winner
    if dealer_score > 21:
        return jsonify({'result': "Dealer busts! You win."})
    elif dealer_score > player_score:
        return jsonify({'result': "Dealer wins!"})
    elif player_score > dealer_score:
        return jsonify({'result': "You win!"})
    else:
        return jsonify({'result': "It's a tie."})

def get_card_value(card):
    if card == 'A':
        return 11
    elif card in ['K', 'Q', 'J']:
        return 10
    else:
        return card

if __name__ == '__main__':
    app.run()
