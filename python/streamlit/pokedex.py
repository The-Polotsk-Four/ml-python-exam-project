import requests
import streamlit as st

local_host = 'http://127.0.0.1:8000'
pokemon_names = ['Show All Pokemon']

res = requests.get(local_host + '/getAllPokemon')
res_json = res.json()

st.set_page_config(
    page_title='pokerdax',
    # layout='centered'
)

# print(res_json[0])
# print(len(res_json))

st.title('Pokéd-Al')
st.text('Welcome to the most advanced pokerdax on the web')

# st.page_link('python/streamlit/clustering.py', label='test')

# st.page_link('./pages/detail_page.py',
#              label='detail',
#              query_params={'pokemon': 'quagsire'})

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
            # pokemon_info = (f'#{pokemon['id']:04d}\n'
            #                 f'{pokemon['name']}\n')
            if len(pokemon['types']) == 1:
                st.page_link('./pages/detail_page.py',
                             label=pokemon['types'][0],
                             query_params={'pokemon': pokemon['name']})
                # pokemon_info = pokemon_info + pokemon['types'][0]
            elif len(pokemon['types']) == 2:
                st.page_link('./pages/detail_page.py',
                             label=pokemon['types'][0] + '/' + pokemon['types'][1],
                             query_params={'pokemon': pokemon['name']})
                # pokemon_info = pokemon_info + pokemon['types'][0] + '/' + pokemon['types'][1]

            # st.text(pokemon_info)

            # st.page_link(detail_page)
            # st.page_link('pages/detail_page.py',
            #              label='test',
            #              query_params={'pokemon': 'quagsire'})
            # def pokedex():
            #     poke_view.page_link('detail_page.py',
            #                  label='test',
            #                  query_params={'pokemon': 'quagsire'})

selected_pokemon = search_bar.selectbox('Choose a pokemon', pokemon_names)

# if selected_pokemon != 'Show All Pokemon':
    # poke_view.empty()
    # for pokemon in res_json:
    #     if pokemon['name'] == selected_pokemon:
    #         render_pokemon(pokemon)
# if selected_pokemon == 'Show All Pokemon':
    # poke_view.empty()
    # for pokemon in res_json:
    #     if pokemon['id'] <= 1025:
    #         render_pokemon(pokemon)
