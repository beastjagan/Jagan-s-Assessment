from flask_restx import Api, Resource, fields, marshal_with, reqparse,Namespace
from database.pokemon_database import Pokemon, db  
from pony.orm import db_session, select, commit, PrimaryKey, Required
from enum import Enum

api = Api()

ns=Namespace("POKEMON")

class PokemonType(Enum): 
    GRASS = 'grass'
    FIRE = 'fire'
    WATER = 'water'
    ELECTRIC = 'electric'

# Request parser for filtering by type
type_parser = reqparse.RequestParser()               
type_parser.add_argument('type', type=str, choices=[t.value for t in PokemonType], help='Filter Pokemon type', required=False)  #specifies that the valid choices for the "type" argument should come from the values of the PokemonType enum.

# Request parser for POST and PATCH
pokemon_parser = reqparse.RequestParser()
pokemon_parser.add_argument("id", type=int, required=True, help="ID cannot be blank for PATCH requests")
pokemon_parser.add_argument("name", type=str, required=True, help="Name cannot be blank")   
pokemon_parser.add_argument("type", type=str, choices=[t.value for t in PokemonType], required=True, help="Filter Pokemon type")
pokemon_parser.add_argument("hp", type=int, required=True, help="HP cannot be blank")

# Request parser for Delete
delete_parser = reqparse.RequestParser()
delete_parser.add_argument('id', type=int, help='ID of the Pokemon to delete', location='json', required=True)


# Pokemon model for marshaling
pokemon_model = api.model('Pokemon', { 
    'id' : fields.Integer(),
    'name': fields.String(),
    'type': fields.String(),
    'hp': fields.Integer()
})

# Resource for listing and adding Pokemon
@ns.route('/')
class PokemonResource(Resource):


    #  GET METHOD - ALL
    # @ns.marshal_with(pokemon_model, as_list=True)
    # @db_session
    # def get(self):
    #     pokemon_list = Pokemon.select()
    #     result = [pokemon.to_dict() for pokemon in pokemon_list]
    #     return result


    #GET METHOD 
    @ns.expect(type_parser)
    @ns.marshal_with(pokemon_model, as_list=True)
    @db_session
    def get(self):
        args = type_parser.parse_args() 
        pokemon_list = Pokemon.select() 
        if args['type']:
            pokemon_list = pokemon_list.filter(type=args['type'])       
        result = [pokemon.to_dict() for pokemon in pokemon_list]
        return result
                                          
          
    
    #POST METHOD - ADD
    @ns.expect(pokemon_model)
    @ns.marshal_with(pokemon_model, code=201)
    @db_session
    def post(self):
        args = pokemon_parser.parse_args()
        name = " ".join(args["name"].split())                               
        pokemon = Pokemon(name=name, type=args["type"], hp=args["hp"])      
        commit()                                                            
        return pokemon, 201



    #PATCH METHOD - UPDATE
    @ns.expect(pokemon_model)
    @ns.marshal_with(pokemon_model)
    @db_session
    def patch(self):
        args = pokemon_parser.parse_args()
        pokemon_id = args['id']
        existing_pokemon = Pokemon.get(id=pokemon_id)
        if not existing_pokemon:
            return {'message': 'Pokemon not found'}, 404
        existing_pokemon.name = " ".join(args["name"].split())
        existing_pokemon.type = args['type']
        existing_pokemon.hp = args['hp']
        commit()
        return existing_pokemon




    # DELETE METHOD - DELETE
    @ns.expect(delete_parser)
    @ns.marshal_with(pokemon_model)
    @db_session
    def delete(self):
        args = delete_parser.parse_args()
        pokemon_id = args['id']
        pokemon = Pokemon.get(id=pokemon_id)
        if not pokemon:
            return {'message': 'Pokemon not found'}, 404
        deleted_pokemon = pokemon.to_dict()
        pokemon.delete()
        commit()
        return deleted_pokemon


















    
  
