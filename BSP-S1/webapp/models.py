#We import the database class
from . import db 


class Deck(db.Model):
    """
    Represent the Deck table of the database
    """
    #the id is the primary key of each entry
    id = db.Column(db.Integer, primary_key=True)
    #Defining a title attributes
    title = db.Column(db.String(50), unique=False)
    #Defining the tag1 and tag2 attributes
    tag1 = db.Column(db.String(30), unique=False)
    tag2 = db.Column(db.String(30), unique=False)
    #Declaring that there will be 2 relatiionships:
    #one with the card table, one with the SP table
    card = db.relationship("Card")
    sp = db.relationship("Space_Repetition")


class Card(db.Model):
    """
    Represent the Card table of the database
    """
    id = db.Column(db.Integer, primary_key=True)
    #Defining a question and answer attributes
    question = db.Column(db.String(1000), unique=False)
    answer = db.Column(db.String(1000), unique=False)
    #Defining a is_in_deck attributes that is 
    # true or false based on if the card is in a deck or not
    is_in_deck = db.Column(db.Boolean, unique=False)
    #A foreign key related to the id of a deck entry in the deck table
    deck_id = db.Column(db.Integer, db.ForeignKey("deck.id"))
    
    
class Space_Repetition(db.Model):
    """
    Represent the Space_Repetition of the database
    """
    id = db.Column(db.Integer, primary_key=True)
    #Defining a grade attribute
    grade = db.Column(db.String(3), unique=False)
    #Definining a date attribute
    date = db.Column(db.DateTime, unique=False)
    #Defining a next date attribute
    priority = db.Column(db.String(10), unique=False)
    #Defining an occurence attribute 
    occurence = db.Column(db.Integer, unique=False)
    #A foreign key related to the id of a deck entry in the deck table
    deck_id = db.Column(db.Integer, db.ForeignKey("deck.id"))
    
    

    