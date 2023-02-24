from flask import Blueprint, flash, render_template, url_for, redirect, request, jsonify
from .models import Card, Deck, Space_Repetition
from . import db
import json
from datetime import datetime

interactions = Blueprint("interactions", __name__)

#Create-Card route
@interactions.route("/createCard", methods=["POST", "GET"])
def createCard():
    #If the https request is a post request
    if request.method == "POST":
        #We save all the request information into variable
        deck_title = request.form.get("deck")
        question = request.form.get("question")
        answer = request.form.get("answer")
        create_multiple = request.form.get("create-multiple")
            
        if not question:
            flash("Your flashcard must have a question", category="error")
            return render_template("createCard.html", Deck=Deck)
        elif not answer:
            flash("Your flashcard must have an answer", category="error")
            return render_template("createCard.html", Deck=Deck)
        #If the deck value is "no-deck"
        if deck_title == "no-deck" or deck_title == None: 
            #We create a card which doesn't belong to a deck
            new_card = Card(question=question, answer=answer, is_in_deck=False)
            #We add the card to the database
            db.session.add(new_card)
            #We commit the change to the database
            db.session.commit()
            
            if not create_multiple:
                #We bring back the user to the inventory page
                return redirect(url_for("views.inventory"))
            else:
                return redirect(url_for("interactions.createCard"))
        else:
            #We add create the card and add it to a deck
            deck_id = Deck.query.filter_by(title=deck_title).first().id
            new_card = Card(question=question, answer=answer, is_in_deck=True, deck_id=deck_id)
            db.session.add(new_card)
            db.session.commit()
            
            if not create_multiple:
                #We bring back the user to the inventory page
                return redirect(url_for("views.inventory"))
            else:
                return redirect(url_for("interactions.createCard"))
    else:
        #If the https request methods is a get request we display the createCard page
        return render_template('createCard.html', Deck=Deck)


#Delete Card Route
@interactions.route("/delete-card/<int:cardId>")
def deleteCard(cardId):
    #We search the card into the database
    card = Card.query.filter_by(id=cardId).first()
    #We delete the card from the database
    db.session.delete(card)
    #We commit change to the database
    db.session.commit()
    #We display a information message to the user
    flash("The card has been deleted", category="success")
    #We bring back the user to the inventory page
    return redirect(url_for("views.inventory"))

#Edit Card Route
@interactions.route("/edit-card/<int:cardId>", methods=["POST", "GET"])
def editCard(cardId):
    #If the https request is a post request
    if request.method == "POST":
        #We save all the request information into variables
        deck_title = request.form.get("deck")
        question = request.form.get("question")
        answer = request.form.get("answer")
        #We search for the card we want to modify
        card = Card.query.filter_by(id=cardId).first()
        if not question:
            flash("Your flashcard must have a question", category="error")
            return render_template("editCard.html", card=card, Deck=Deck)
        elif not answer:
            flash("Your flashcard must have an answer", category="error")
            return render_template("editCard.html", card=card, Deck=Deck)
        #If the card has no deck
        if deck_title == "no-deck": 
            #We apply changes and remove the card from a deck
            card.is_in_deck = False
            card.deck_id = None
            card.question = question
            card.answer = answer
            db.session.add(card)
            db.session.commit()
            flash("Your card has been modified", category="success")
            return redirect(url_for("views.inventory"))
        else:
            #We apply the change and add the card to a deck
            deck_id = Deck.query.filter_by(title=deck_title).first().id
            card.is_in_deck = True
            card.question = question
            card.answer = answer
            card.deck_id = deck_id
            db.session.add(card)
            db.session.commit()
            flash("Your card has been modified", category="success")
            return redirect(url_for("views.inventory"))
    else:
        #If it's a get request we search for the card and bring the user to the edit page
        card = Card.query.filter_by(id=cardId).first()
        return render_template("editCard.html", card=card, Deck=Deck)
    

#Create Deck Route
@interactions.route("/createDeck", methods=["GET", "POST"])
def createDeck():
    #If the http request is a post request
    if request.method == "POST":
        #We save all the request informations in variables
        title = request.form.get("title")
        tag1 = request.form.get("tag1")
        tag2 = request.form.get("tag2")
        if not title:
            flash("Your deck must have a title", category="error")
            return render_template("createDeck.html", Card=Card)

        #We create the deck, add it to the database and commit the changes
        new_deck = Deck(title=title, tag1=tag1, tag2=tag2)
        db.session.add(new_deck)
        db.session.commit()
        #We make a dictionary which have card id as key and card as value for all card that have no deck
        id_dict = {card.id: card for card in Card.query.filter_by(is_in_deck=False).all()}
        #We make a list of card for all card that the user wants to add to the deck
        cards = [card for id, card in id_dict.items() if request.form.get(str(id)) == "on"]
        #We itterate throught the list of card chose by the user
        for card in cards:
            #Change the is in deck property to true
            card.is_in_deck = True
            #Add the card to the deck
            card.deck_id = Deck.query.filter_by(title=title).first().id
            #Add the overwritten card's data to the database
            db.session.add(card)
            #Commit the change
            db.session.commit()
            
        #redirect the user to the dashboard page
        return redirect(url_for("views.inventory"))     
    else:
        #If it is a get request -> display the create deck page
        return render_template("createDeck.html", Card=Card)
    
    
#Delete Deck Route
@interactions.route("/delete-deck/<int:deckId>")
def deleteDeck(deckId):
    #We search the deck using his ID
    deck = Deck.query.filter_by(id=deckId).first()
    #We itterate through all the cards belonging to the deck
    for card in Card.query.filter_by(deck_id=deckId).all():
        #We delete each card belonging to the deck
        db.session.delete(card)
        db.session.commit()
    
    #Finally we delete the deck
    db.session.delete(deck)
    db.session.commit()
    
    return redirect(url_for("views.inventory"))


#Edit Deck Route
@interactions.route("/edit-deck/<int:deckId>" , methods=["POST", "GET"])
def editDeck(deckId):
    #Check which http method is used
    if request.method == "POST":
        #We search for the deck using his ID
        deck = Deck.query.filter_by(id=deckId).first()
        #We get the request data
        title = request.form.get("title")
        tag1 = request.form.get("tag1")
        tag2 = request.form.get("tag2")
        
        if not title:
            flash("Your deck must have a title", category="error")
            return render_template("editDeck.html", deck=Deck.query.filter_by(id=deckId).first(), Card=Card)

        #Update the deck
        deck.title = title
        deck.tag1 = tag1
        deck.tag2 = tag2
        db.session.add(deck)
        db.session.commit()
        
        #We make a dictionary which have card id as key and card as value for all card that have no deck
        cardsWithNoDeck = {card.id: card 
                           for card in Card.query.filter_by(is_in_deck=False).all()
                           }
        #We make a list of card for all card that the user wants to add to the deck
        needToBeAddedCards = [
                            card 
                            for id, card in cardsWithNoDeck.items() 
                            if request.form.get(str(id)) == "on"
                            ] 
        cardsInDeck = [card 
                       for card in Card.query.filter_by(deck_id=deckId)]
        
        needToBeRemovedCards = [card for card in cardsInDeck
                                if not request.form.get(str(card.id))]
        
        #We itterate throught the list of card that the user wants to add to the deck
        for card in needToBeAddedCards:
            #Change the is in deck property to true
            card.is_in_deck = True
            #Add the card to the deck
            card.deck_id = deckId
            db.session.add(card)
            db.session.commit()
        
        #We itterate throught the list of card that the user wants to remove from the deck
        for card in needToBeRemovedCards:
            #Change the is in deck property to False
            card.is_in_deck = False
            #Remove the card from the deck
            card.deck_id = None
            db.session.add(card)
            db.session.commit()
        
        return redirect(url_for("views.inventory"))
    
    else:
        return render_template("editDeck.html", deck=Deck.query.filter_by(id=deckId).first(), Card=Card)
    
    
#Route for deck review
@interactions.route("/review-deck/<int:deckId>")
def reviewDeck(deckId):
    deck = Deck.query.filter_by(id=deckId).first()
    cards = [card for card in Card.query.filter_by(deck_id=deckId)]
    return render_template("review.html", deck=deck, cards=cards)


@interactions.route("/result", methods=["POST"])
def displayResult():
    if request.method == "POST":
        data = json.loads(request.data)
        deck_id = data["deckID"]
        grade = data["grade"]
        
        existing_session = Space_Repetition.query.filter_by(deck_id=deck_id).first()
        if grade <= 25:
            priority = "red"
        elif grade <= 50:
            priority = "yellow"
        elif grade <= 75:
            priority = "green"
        else:
            priority = "white"
        if existing_session:
            existing_session.date = datetime.now()
            existing_session.occurence += 1
            existing_session.grade = grade
            existing_session.priority = priority
        else:
            new_rep = Space_Repetition(grade=grade,
                                       date=datetime.now(), 
                                       priority=priority, 
                                       occurence=1, 
                                       deck_id=deck_id)
            db.session.add(new_rep)
            
        db.session.commit()
        
        return jsonify({})
    

