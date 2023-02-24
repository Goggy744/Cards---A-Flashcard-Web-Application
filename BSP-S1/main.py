#Import the create_app function from __init__.py
from webapp import create_app

#If the file runned is not an imported one we run the code
if __name__ == "__main__":
    #We create the app 
    app = create_app()
    #We run the app as a localhost on the port 8000
    app.run(host="localhost", port="8000")