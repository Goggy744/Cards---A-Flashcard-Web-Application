#Importing all the needed libraries and function
from flask import Blueprint, render_template
from .models import Card, Deck, Space_Repetition

#We create the views Blueprint
views = Blueprint("views", __name__)
    
def space_rep_algo():
    """
    Function that create a list of deck IDS that the user must review in priority
    """
    #Declare the list of review session
    session_l = [session for session in Space_Repetition.query.all()]
    #We define an empty list
    must_review = []
    #We define a list of priority
    priority_l = ["red", "yellow", "green", "white", "finish"]
    #We define a session index and priority index that refers to both list
    sessionIndex = 0
    priorityIndex = 0
    
    #While loop until the element of the priority list at the priority index is "finish"
    while priority_l[priorityIndex] != "finish":
        #Check the priority attribute of the session
        if session_l[sessionIndex].priority == priority_l[priorityIndex]:
            #We append the deck ID to the must review list if it is the good priority
            must_review.append(session_l[sessionIndex].deck_id)
        #Increment the session index by 1
        sessionIndex += 1
        #Check if sessionIndex is equal to the lenght of the session list
        if sessionIndex == len(session_l):
            #If it is we reset the sessionIndex
            sessionIndex = 0
            #And we increment the priority index by 1
            priorityIndex += 1
            
    #we return the 3 first element of the must review list 
    return must_review[:3]
    
        

        

#LandingPage Route
@views.route("/")
def landingPage():
    """
    Function that displays the landingPage
    """
    #display the html page refering to the landing page
    return render_template("landingPage.html")


#Dashboard Route
@views.route("/dashboard")
def dashboard():
    """
    Functions that displays the dashboard page
    """
    #We create a list of all the deck id the user reviwed
    reviewSession = [session.deck_id for session in Space_Repetition.query.all()]
    #We get all the decks
    decks = Deck.query.all()
    #Check if the lenght of the list of deck id reviewed is less or equal than 3
    if len(reviewSession) <= 3:
        #If yes, we create a list of all the deck that correspond to the list of deck id
        lastDeckRev = [deck for deck in decks if deck.id in reviewSession]
    else:
        #Else we take only the 3 first
        lastDeckRev = [deck for deck in decks if deck.id in reviewSession[len(reviewSession)-3:]]
           
    if len([session for session in Space_Repetition.query.all()]) != 0:
        #Create a list of deck that the user must review soon
        mustReview = [Deck.query.filter_by(id=deckId).first() for deckId in space_rep_algo()]
    else:
        mustReview = []
        
    #return the html page
    return render_template("dashboard.html", lastDeckRev=lastDeckRev, mustReview=mustReview)


#Inventory Route
@views.route("/inventory", methods = ["POST", "GET"])
def inventory():
    """
    Function that display the inventory page
    """
    #We display the inventory page
    return render_template("inventory.html", Card=Card, Deck=Deck)
