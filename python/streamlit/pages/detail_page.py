import streamlit as st
import requests
import os
import dotenv

dotenv.load_dotenv()

st.title("Pokemon Detail")

st.page_link('pokedex.py', label='home')

selected_name = st.query_params['pokemon']

local_host = os.getenv("FAST_API_URL", "http://127.0.0.1:8000")

res=requests.get(f'{local_host}/getAllPokemon')
all_pokemon = res.json()

pokemon_names = [pokemon["name"] for pokemon in all_pokemon]

pokemon_basic = next(p for p in all_pokemon if p["name"] == selected_name)

pokeapi_res = requests.get(f'https://pokeapi.co/api/v2/pokemon/{selected_name}')
pokemon = pokeapi_res.json()

st.image(pokemon_basic['sprite'], width=150, caption=selected_name)

st.header(pokemon['name'].capitalize())
type_str = ' / '.join([t["type"]['name'].capitalize() for t in pokemon["types"]])
st.write(f'**Type:** {type_str}')

st.divider()

st.subheader("Base Stats")
stat_map={s['stat']['name']: s['base_stat'] for s in pokemon["stats"]}

stats = {
    "HP": stat_map.get("hp", 0),
    "Attack": stat_map.get("attack", 0),
    "Defense": stat_map.get("defense", 0),
    "Sp. Atk": stat_map.get("special-attack", 0),
    "Sp. Def": stat_map.get("special-defense", 0),
    "Speed": stat_map.get("speed", 0),
}

for stat_name, stat_value in stats.items():
    col1, col2 = st.columns([1, 3])
    col1.write(f"**{stat_name}**")
    col2.progress(stat_value / 255, text=str(stat_value))

st.divider()

st.subheader("Info")
col1, col2 = st.columns(2)
col1.metric("Height", f"{pokemon['height'] / 10} m")
col2.metric("Weight", f"{pokemon['weight'] / 10} kg")
base_total = sum(s["base_stat"] for s in pokemon["stats"])
col1.metric("Base Stat", base_total)
