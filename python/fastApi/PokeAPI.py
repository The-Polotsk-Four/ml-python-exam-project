import requests
import json
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse

# to run, use
# uvicorn PokeAPI:app --reload

pokemon_cache = []

@asynccontextmanager
async def lifespan(app: FastAPI):
    # this function runs on fastapi startup and checks if there is any cached information
    # if cache is empty it calls the build_pokemon_cache and gets all the information needed
    global pokemon_cache
    if os.path.exists('pokemon_cache.json'):
        with open('pokemon_cache.json') as f:
            pokemon_cache = json.load(f)
    else:
        pokemon_cache = build_pokemon_cache()
    yield

# creates fastapi app and runs the lifespan on startup
app = FastAPI(lifespan=lifespan)

def build_pokemon_cache():
    # the query is the json that gets sent using GraphQL
    # this query extracts the pokemon id, name, typings and all sprites
    query = """
    {
      pokemon_v2_pokemon(limit: 1350) {
        id
        name
        pokemon_v2_pokemontypes {
          pokemon_v2_type { name }
        }
        pokemon_v2_pokemonsprites {
          sprites
        }
      }
    }
    """

    # api call to pokeapi
    res = requests.post(
        'https://beta.pokeapi.co/graphql/v1beta',
        json={'query': query}
    )
    # all the raw json data
    raw_json = res.json()['data']['pokemon_v2_pokemon']

    allPokemon = []
    # cycles through the raw_json data and saves the information in allPokemon
    for pokemon in raw_json:
        sprites = pokemon['pokemon_v2_pokemonsprites'][0]['sprites']
        allPokemon.append({
            'id': pokemon['id'],
            'name': pokemon['name'],
            'types': [type['pokemon_v2_type']['name'] for type in pokemon['pokemon_v2_pokemontypes']],
            'sprite': sprites.get('front_default')
        })
    # saves allPokemon in pokemon_cache.json so it's locally stored 
    # so we dont need to make more api calls
    with open('pokemon_cache.json', 'w') as f:
        json.dump(allPokemon, f)

    return allPokemon

@app.get('/getAllPokemon')
def get_pokemon():
    return JSONResponse(
        content=pokemon_cache
    )


@app.get('/getSpecificPokemon/{pokemon}')
def getPokemon(pokemon: str ):
    
    apiUrl = f'https://pokeapi.co/api/v2/pokemon/{pokemon}'
    
    res = requests.get(apiUrl)

    data = res.json()

    return data
