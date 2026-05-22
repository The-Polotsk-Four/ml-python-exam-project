# Pokedex exam project
This pokedex is made for the EK python and machine learning exams summer 2026

Made by: [Gustav](https://github.com/GusViking), [Sofus](https://github.com/SofusVingaard) and [Tobias](https://github.com/itsHarning)

## Installation
If you have docker installed, you can run `docker compose up --build` in the root of the project to run everything


If not, to install requirements you can use

```bash
# If you have uv installed
uv sync

# If uv isn't installed, use pip
pip install -r requirements.txt
```
then use the following to run the application
```bash
# To run the api use 
uvicorn python.fastApi.PokeAPI:app --reload

# To run the streamlit use 
streamlit run ./python/streamlit/pokedex.py
```

## Usage
### Pokedex
On the pokedex page you can choose a Pokémon from the dropdown menu, or click on any of the text of the Pokémon to go to a more detailed page with a handful of stats about it.

### Clustering

### Chat with Pikachu

### Recognise Pokémon