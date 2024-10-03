# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Pet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

# add views here 
#creating a route to the index page
@app.route("/")
def index():
    response = make_response(
        "<h1>Welcome to the pet directory!</h1>",
        200
    )
    return response

# Creating a route where you can search a pet by the id
@app.route("/pets/<int:id>")
def pet_by_id(id):
    # filtering the Pet model  using the id
    pet = Pet.query.filter(Pet.id == id).first()

    #an if statement to check whether the pet id is in the datbase
    if pet:
        response_body = f"<p>{pet.name} {pet.species}</p>"
        response_status = 200
    else:
        response_body = f"<p>Pet {id} not found</p>"
        response_status = 200
    
    response = make_response(response_body, response_status)
    return response

# creating a route for the species
@app.route("/species/<string:species>")
def pet_by_species(species):
    #querying the pet by the species
    pets = Pet.query.filter_by(species = species).all()

    #getting the length of the pets with the same species name
    size = len(pets)
    response_body = f"<h1>There are {size} {species}</h1>"

    # looping through the pets with the same species to view their names
    for pet in pets:
        response_body += f"<p>{pet.name}</p>"
    response = make_response(response_body, 200)
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
