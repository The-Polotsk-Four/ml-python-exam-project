from fastapi import FastAPI
import requests
import json

app = FastAPI()

@app.get('/getAllPokemon')
def getPokemon():
    apiUrl = 'https://pokeapi.co/api/v2/pokemon?limit=1350'
    
    res = requests.get(apiUrl)

    data = res.json()

    pokemonInformation = []

    for pokemonData in data['results']:
        pokemonName = pokemonData['name']
        pokemonInformation.append(pokemonName)

    print(pokemonInformation)

    # important information for the specific pokemon
    # name, stats, typings, sprite, pokedex entry



    return data



@app.get('/getSpecificPokemon/{pokemon}')
def getPokemon(pokemon: str ):
    
    apiUrl = f'https://pokeapi.co/api/v2/pokemon/{pokemon}'
    
    res = requests.get(apiUrl)

    data = res.json()

    return data
