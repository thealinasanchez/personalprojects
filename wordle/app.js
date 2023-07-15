//
// Variable Initialization:
var guessDiv = document.querySelector("#guessDiv");
var text_input = document.querySelector("#text-input");
var submit_button = document.querySelector("submit-button");
var correctWord = "";
var validWords = [];
var possibleAnswers = [];
var guessedWords = [];
var NUM_GUESSES = 6;
var WORD_LENGTH = 5;
var GAME_OVER = false;
var keyboardWord = "";

function getCurrentWord() {
  var dateString = moment().format("YYYYMMDDHHmm");
  var dateNumber = parseInt(dateString, 10);
  var word = possibleAnswers[dateNumber % possibleAnswers.length];
  console.log(word);
  return word;
}

function pickRandomWord() {
  var randomIndex = Math.floor(possibleAnswers.length * Math.random());
  correctWord = possibleAnswers[randomIndex];
  console.log(correctWord);
}

function chooseNewWord() {
  var newWord = getCurrentWord();
  if (!correctWord || correctWord != newWord) {
    resetGame();
    correctWord = newWord;
    saveState();
    console.log("The answer is now: ", correctWord);
  } else {
    console.log("The answer is still: ", correctWord);
  }
}

function getWordList() {
  fetch(
    "https://raw.githubusercontent.com/chidiwilliams/wordle/main/src/data/words.json"
  ).then(function (response) {
    response.json().then(function (data) {
      console.log(data);
      possibleAnswers = data;
      validWords = data;
      // console.log(validWords);
      loadState();
      chooseNewWord();
      updateGuesses();
      saveState();
    });
  });
}
//
// updateGuesses Function:
function updateGuesses() {
  var allGuessesDiv = document.querySelector("#guessesDiv");

  allGuessesDiv.innerHTML = "";

  for (var i = 0; i < NUM_GUESSES; i++) {
    // i is each word
    var newGuess = document.createElement("div");
    newGuess.classList.add("guess");
    var checkedOutput;
    if (i < guessedWords.length) {
      checkedOutput = checkWord(guessedWords[i], correctWord);
      newGuess.classList.add("guessed");
    }
    //
    for (var j = 0; j < WORD_LENGTH; j++) {
      // j is each letter in the word
      var newLetter = document.createElement("span");
      newLetter.classList.add("letter");
      if (i < guessedWords.length) {
        // as long as the word is part of the list of guessed words, then add to a row
        newLetter.innerHTML = guessedWords[i][j];
        //
        //create a variable that uses checkWord function
        checkedOutput = checkWord(guessedWords[i], correctWord);
        console.log(checkedOutput);
        //
        //
        // if letter in checkedOutput is 1 (if it is correct/green)
        if (checkedOutput[j] == 1) {
          newLetter.classList.add("match");
        } else if (checkedOutput[j] == 2) {
          // if letter in checkedOutput is 2 (if it is almost correct/yellow)
          newLetter.classList.add("contains");
        }
      } else if (i == guessedWords.length) {
        if (j < keyboardWord.length) {
          newLetter.innerHTML = keyboardWord[j];
        }
      }

      newGuess.appendChild(newLetter);
    }

    allGuessesDiv.appendChild(newGuess);
  }
}

function makeGuess() {
  var guessInput = document.querySelector("#guess-input");
  var messageDiv = document.querySelector("#message");
  //
  if (!GAME_OVER) {
    if (keyboardWord.length != 5) {
      messageDiv.innerHTML = "5 letters please.";
    } else if (!validWords.includes(keyboardWord)) {
      messageDiv.innerHTML = "Not a real word.";
    }

    // if the input IS in valid words list or correct word
    else {
      // creates a last guess input value
      var lastGuess = keyboardWord;
      // add last guess to guessedWords list
      guessedWords.push(lastGuess);
      // after adding, reset user input back to empty
      keyboardWord = "";
      // is lastGuess is correct (all green)
      if (lastGuess == correctWord) {
        messageDiv.innerHTML = "You Win!";
        GAME_OVER = true;
      }
      // if not correct, go back to default nothing
      else {
        messageDiv.innerHTML = "";
      }
      updateGuesses();
      saveState();
    }
    if (guessedWords.length >= NUM_GUESSES && !GAME_OVER) {
      GAME_OVER = true;
      messageDiv.innerHTML = "You lose! Correct answer was: " + correctWord;
    }
  }
}

function setupKeys() {
  var currentWordDiv = document.querySelector("#current-word");
  document.onkeydown = function (event) {
    console.log(event);
    if (event.key == "Enter") {
      makeGuess();
    } else if (event.keyCode >= 65 && event.keyCode <= 90) {
      if (keyboardWord.length < 5) {
        keyboardWord += event.key;
        console.log("current guess: ", keyboardWord);
      }
      if (keyboardWord.length == 5) {
        makeGuess();
      }
    } else if (event.key == "Backspace") {
      keyboardWord = keyboardWord.slice(0, -1);
      console.log(keyboardWord);
    } else {
      console.log(event.key);
    }

    if (!GAME_OVER) {
      currentWordDiv.innerHTML = keyboardWord;
      updateGuesses();
    }
  };
}

getWordList();
updateGuesses();
setupKeys();
makeGuess();

// checkWord Function:
function checkWord(guessedWord, rightWord) {
  var checkArray = [0, 0, 0, 0, 0];

  var correctLetters = rightWord.split("");
  // if guessedWord[i] is in same position as rightWord[i]
  for (var i = 0; i < WORD_LENGTH; i++) {
    console.log(guessedWord[i], correctLetters[i]);
    if (guessedWord[i] == correctLetters[i]) {
      checkArray[i] = 1;
      correctLetters[i] = null;
    }
  }
  // if guessedWord[i] is in correctLetters in general
  for (var i = 0; i < WORD_LENGTH; i++) {
    var index = correctLetters.indexOf(guessedWord[i]);
    if (index >= 0 && checkArray[i] == 0) {
      checkArray[i] = 2;
      correctLetters[index] = null;
    }
  }

  return checkArray;
}

function saveState() {
  localStorage.setItem("correctWord", JSON.stringify(correctWord));
  localStorage.setItem("guessedWords", JSON.stringify(guessedWords));
  localStorage.setItem("GAME_OVER", JSON.stringify(GAME_OVER));
}

function loadState() {
  correctWord = JSON.parse(localStorage.getItem("correctWord"));
  guessedWords = JSON.parse(localStorage.getItem("guessedWords"));
  GAME_OVER = JSON.parse(localStorage.getItem("GAME_OVER"));
  //what if they're empty tho?
  if (!guessedWords) {
    guessedWords = [];
  }
  if (!GAME_OVER) {
    GAME_OVER = false;
  }
}

function resetGame() {
  correctWord = "";
  currentGuess = "";
  guessedWords = [];
  GAME_OVER = false;
}
// Word of advice: might have to do something for a case dealing with 2 o's and
// one is in the right place and one isn't and stuff like that.