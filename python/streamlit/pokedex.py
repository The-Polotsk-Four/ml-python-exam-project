import requests
import streamlit as st

local_host = 'http://127.0.0.1:8000'
pokemon_names = ['Show All Pokemon']

res = requests.get(local_host + '/getAllPokemon')
res_json = res.json()

st.set_page_config(
    page_title='pokerdax',
    layout='centered'
)

# print(res_json[0])
# print(len(res_json))

st.title('Pokéd-Al')
st.text('Welcome to the most advanced pokerdax on the web')

def render_pokemon(given_pokemon):
    pokemon_names.append(given_pokemon['name'])
    with pokedex.container():
        with poke_view.container():
            # st.write(pokemon)
            st.image(given_pokemon['sprite'])
            st.write(f'#{given_pokemon['id']:04d}')
            st.write(given_pokemon['name'])
            if len(given_pokemon['types']) == 1:
                st.write(given_pokemon['types'][0])
            elif len(given_pokemon['types']) == 2:
                st.write(given_pokemon['types'][0] + '/' + given_pokemon['types'][1])
            # st.write(len(pokemon['types']))

search_bar = st.container()
pokedex = st.empty()
poke_view = st.empty()

for pokemon in res_json:
    if pokemon['id'] <= 1025:
        render_pokemon(pokemon)

selected_pokemon = search_bar.selectbox('Choose a pokemon', pokemon_names)

if selected_pokemon != 'Show All Pokemon':
    pokedex.empty()
    poke_view.empty()
    for pokemon in res_json:
        if pokemon['name'] == selected_pokemon:
            render_pokemon(pokemon)
if selected_pokemon == 'Show All Pokemon':
    pokedex.empty()
    poke_view.empty()
    for pokemon in res_json:
        if pokemon['id'] <= 1025:
            render_pokemon(pokemon)
