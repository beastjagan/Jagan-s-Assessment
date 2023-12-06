from flask import Flask
from flask_restx import Api, Resource, fields
from methods.pokemon_methods import api, ns as UserPoki
from database.pokemon_database import db


api.add_namespace(UserPoki)

app = Flask(__name__)
api.init_app(app)


if __name__ == '__main__':
    app.run(debug=True)





  

 