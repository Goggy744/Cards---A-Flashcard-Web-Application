#Importing all the libraries needed
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path, stat

#Initialize the database class and filename
db = SQLAlchemy()
#Defining the constant DBNAME that represente the name of the database
DBNAME = "database.db"

#Declaring the function that will generate the app
def create_app():
    """
    Function that generate the app 
    """
    #Setting up the app
    app = Flask(__name__)
    app.secret_key = "some random text"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DBNAME}"
    #We link the database to the app
    db.init_app(app)

    
    # Importing the differents blueprints
    from .views import views
    from .interactions import interactions

    # Registering the differents blueprints
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(interactions, url_prefix="/")

    #Create the database
    create_database(app)
        
    #Return the app
    return app

    
def create_database(app):
    """
    Function that will create the database if it wasn't created yet 
    """
    #If there is no database in the webapp directory we create it else nothing happens
    if not path.exists('webapp/database.db'):
        db.create_all(app=app)
        print("database created")

