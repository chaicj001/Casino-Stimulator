const dealerHandElem = document.getElementById("dealer-hand");
const dealerScoreElem = document.getElementById("dealer-score");
const playerHandElem = document.getElementById("player-hand");
const playerScoreElem = document.getElementById("player-score");
const outcomeElem = document.getElementById("outcome");

function clearTable() {
  dealerHandElem.innerHTML = "";
  dealerScoreElem.innerHTML = "";
  playerHandElem.innerHTML = "";
  playerScoreElem.innerHTML = "";
  outcomeElem.innerHTML = "";
}

function updateScores(playerScore, dealerScore) {
  playerScoreElem.innerHTML = `Player score: ${playerScore}`;
  dealerScoreElem.innerHTML = `Dealer score: ${dealerScore}`;
}

function updateCards(cards, elem) {
  elem.innerHTML = "";
  for (let i = 0; i < cards.length; i++) {
    const cardElem = document.createElement("img");
    cardElem.src = `cards/${cards[i]}.png`;
    elem.appendChild(cardElem);
  }
}

function displayOutcome(result) {
  outcomeElem.innerHTML = result;
}

function play() {
  // Clear the table
  clearTable();

  // Get the user's choice of "hit" or "stand"
  const selectedChoice = document.querySelector('input[name="choice"]:checked');
  if (!selectedChoice) {
    displayOutcome("Please select 'hit' or 'stand'.");
    return;
  }
  const choice = selectedChoice.value;

  // Call the /play_blackjack endpoint to play the game
  fetch("/play_blackjack", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ choice })
  })
    .then((response) => response.json())
    .then((data) => {
      // Display the cards and scores
      updateCards(data.dealer_hand, dealerHandElem);
      updateCards(data.player_hand, playerHandElem);
      updateScores(data.player_score, data.dealer_score);

      // Display the outcome
      displayOutcome(data.result);
    });
}

document.getElementById("play-btn").addEventListener("click", play);
