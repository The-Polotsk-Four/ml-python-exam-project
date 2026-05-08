import requests
import streamlit as st

local_host = 'http://127.0.0.1:8000'

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

for pokemon in res_json:
    with st.container():
        if pokemon['id'] <= 1025:
            # st.write(pokemon)
            if pokemon['sprite']:
                st.image(pokemon['sprite'])
                st.write(f'#{pokemon['id']:04d}')
                st.write(pokemon['name'])
                if len(pokemon['types']) == 1:
                    st.write(pokemon['types'][0])
                elif len(pokemon['types']) == 2:
                    st.write(pokemon['types'][0] + '/' + pokemon['types'][1])
                #st.write(len(pokemon['types']))
