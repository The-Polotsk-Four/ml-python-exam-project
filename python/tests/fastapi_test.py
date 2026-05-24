import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'fastApi'))

from fastapi.testclient import TestClient
from PokeAPI import app

client = TestClient(app)

def test_get_all_pokemon():
    response = client.get('/getAllPokemon')
    assert response.status_code == 200


def test_get_specific_pokemon_pikachu():
    response = client.get('/getSpecificPokemon/pikachu')

    assert response.status_code == 200
    assert response.json()['name'] == 'pikachu'

def test_get_specific_pokemon_squirtle():
    response = client.get('/getSpecificPokemon/squirtle')

    assert response.status_code == 200
    assert response.json()['name'] == 'squirtle'

def test_no_pokemon_selected():
    response = client.get('/getSpecificPokemon')

    assert response.status_code == 404


