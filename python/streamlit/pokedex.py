import streamlit as st
from plotly.graph_objs.layout import title

st.title('Pokéd-Al')
st.text('Welcome to the most advanced pokerdax on the web')

amountOfPokemon = 151
pokemon = 0
columnIndex = 0

c1, c2, c3, c4, c5, c6 = st.columns([1, 1, 1, 1, 1, 1], gap="small")

row_001 = st.columns(6)

column_list = []

while pokemon < amountOfPokemon:
    if pokemon % 6 == 0:
        print('index: {:d}'.format(columnIndex))
        # print(pokemon)
        column_list.append(st.columns(6))
        columnIndex += 1
    print('pokemon: {:d}'.format(pokemon))

    pokemon += 1

for column in column_list:
    print(column)
    for container in column_list[column]:
        tile = container.container()
        tile.title(column)