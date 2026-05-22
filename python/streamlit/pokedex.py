import requests
import streamlit as st
import os
import dotenv

dotenv.load_dotenv()

local_host = os.getenv("FAST_API_URL", "http://127.0.0.1:8000")

pokemon_names = ['Show All Pokemon']

res = requests.get(local_host + '/getAllPokemon')
res_json = res.json()

st.set_page_config(
    page_title='pokerdax'
)

st.title('Pokéd-Al')
st.text('Welcome to the most advanced pokerdax on the web')

search_bar = st.container()
poke_view = st.container()

for pokemon in res_json:
    if pokemon['id'] <= 1025:
        pokemon_names.append(pokemon['name'])
        with poke_view.container(border=True, horizontal_alignment="center"):
            st.image(pokemon['sprite'])
            st.page_link('./pages/detail_page.py',
                         label=f'#{pokemon['id']:04d}',
                         query_params={'pokemon': pokemon['name']})
            st.page_link('./pages/detail_page.py',
                         label=pokemon['name'],
                         query_params={'pokemon': pokemon['name']})
            if len(pokemon['types']) == 1:
                st.page_link('./pages/detail_page.py',
                             label=pokemon['types'][0],
                             query_params={'pokemon': pokemon['name']})
            elif len(pokemon['types']) == 2:
                st.page_link('./pages/detail_page.py',
                             label=pokemon['types'][0] + '/' + pokemon['types'][1],
                             query_params={'pokemon': pokemon['name']})

selected_pokemon = search_bar.selectbox('Choose a pokemon', pokemon_names)
