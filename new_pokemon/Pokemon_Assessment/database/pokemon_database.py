from pony.orm import Database, Required, PrimaryKey

db = Database()

class Pokemon(db.Entity):
    _table_ = 'pokemon'
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    type = Required(str)
    hp = Required(int)

db.bind(provider='sqlite', filename='pokedex.sqlite', create_db=True)
db.generate_mapping(create_tables=True)


