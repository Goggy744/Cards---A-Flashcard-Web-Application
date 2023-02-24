//Get a list of cards
let cards = document.querySelectorAll(".card-inner");
//Loop through the list of cards
cards.forEach( (card) => {
    //Add a click event listener 
    card.addEventListener("click", handleClick  = () => {
        //check if the scond child of the card has the hide class
        if (card.childNodes[1].classList.contains("hide")) {
            //Add the class hide
            card.childNodes[3].classList.add("hide")
            //Remove the class hide
            card.childNodes[1].classList.remove("hide")
        } else {
            //remove the class hide
            card.childNodes[3].classList.remove("hide")
            //Add the class hide
            card.childNodes[1].classList.add("hide")
        }
    })
})
