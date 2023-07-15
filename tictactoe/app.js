var all_tiles = document.querySelectorAll(".tile");
console.log(all_tiles);
console.log(all_tiles.length);

var winnerDiv = document.querySelector("#winner");
console.log(winnerDiv);

var turns = document.querySelector("#turns");
console.log(turns);

var playerTurn = 0;
var gameOver = false;

function checkWinner(player) {
  var winningList = [
    "row1",
    "row2",
    "row3",
    "col1",
    "col2",
    "col3",
    "diag1",
    "diag2",
  ];

  var winner = false;

  winningList.forEach(function (item) {
    var selector = "." + item + "." + player;
    var tiles = document.querySelectorAll(selector);
    console.log("Selector:", selector, "count:", tiles.length);

    if (tiles.length == 3) {
      turns.innerHTML = "";
      winner = true;
      winnerDiv.innerHTML = "player " + player + " wins!";
    }
  });

  return winner;
}

all_tiles.forEach(function (tile) {
  tile.onclick = function () {
    if (tile.innerHTML == "" && !gameOver) {
      if (playerTurn == 0) {
        tile.innerHTML = "O";
        tile.classList.add("blue");
        tile.classList.add("O");
        turns.innerHTML = "Player X's turn!";
        playerTurn = 1;
      } else {
        tile.innerHTML = "X";
        tile.classList.add("red");
        tile.classList.add("X");
        turns.innerHTML = "Player O's turn!";
        playerTurn = 0;
      }

      if (checkWinner("X")) {
        console.log("X HAS WON!");
        winnerDiv.classList.add("X");
        gameOver = true;
      }

      if (checkWinner("O")) {
        console.log("O HAS WON!");
        winnerDiv.classList.add("O");
      }
    }
    if (tile.innherHTML == gameOver) {
    }
  };
});