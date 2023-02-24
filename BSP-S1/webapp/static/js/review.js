//Select all the element that has the class card-item
const cardsItem = document.querySelectorAll(".card-item");

const prev = (index) => {
    if (index > 1) {
        let cardToHide = document.getElementById(index)
        index = (parseInt(index) - 1).toString()
        let cardToShow = document.getElementById(index)
        cardToHide.classList.remove("displayed")
        cardToHide.classList.add("hide")
        cardToShow.classList.remove("hide")
        cardToShow.classList.add("displayed")}}

/*Function that show the next card*/
const next = (index) => {
    //check if the index is less than the number of cards
    if (index < cardsItem.length) {
        //Assign a variable using the index for the card we want to hide
        let cardToHide = document.getElementById(index)
        //Incremente the index by 1 and transform it to a string
        index = (parseInt(index) + 1).toString()
        //Assign a variable using the new index for the card we want to show
        let cardToShow = document.getElementById(index)
        //Remove the class displayed to the card we want to hide
        cardToHide.classList.remove("displayed")
        //add the class hide to the card we want to hide
        cardToHide.classList.add("hide")
        //Remove the class hide to the card we want to show
        cardToShow.classList.remove("hide")
        //Add the class displayed to the card we want to show
        cardToShow.classList.add("displayed")
    }
}

const checkAnswer = (btn, cardID) => {
    let card = document.getElementById("card-"+cardID)
    if (card.innerHTML == "" && btn.classList.contains("failed")) {
        card.innerHTML = "0"
    } else if (card.innerHTML == "" && btn.classList.contains("passed")) {
        card.innerHTML = "1"
    }
}

const stop = (deckID) => {
    let scoreEl = document.getElementById("score")
    let wrongAnswerCount = 0
    let rightAnswerCount = 0
    let answerCount = 0
    scoreEl.childNodes.forEach( el => {
        if (el.innerHTML == "0") {
            wrongAnswerCount += 1
            answerCount += 1
        } else if (el.innerHTML == "1") {
            rightAnswerCount += 1
            answerCount +=1 }})
    grade = rightAnswerCount*100 / answerCount

    fetch("../result", {
        method: "POST",
        body: JSON.stringify({grade: grade, deckID: deckID})
    //redirect the user to the dashboard page
    }).then((_res) => { window.location.href = "/dashboard"; })}
