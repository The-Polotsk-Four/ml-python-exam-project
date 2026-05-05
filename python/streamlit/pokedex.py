import requests
import streamlit as st

local_host = 'http://127.0.0.1:8000'

res = requests.get('http://127.0.0.1:8000/getAllPokemon')
res_json = res.json()

print(res_json[0])
print(len(res_json))

st.title('Pokéd-Al')
st.text('Welcome to the most advanced pokerdax on the web')

for pokemon in res_json:
    with st.container():
        if pokemon['id'] <= 1025:
            st.write(pokemon)
            if pokemon['sprite']:
                st.image(pokemon['sprite'])