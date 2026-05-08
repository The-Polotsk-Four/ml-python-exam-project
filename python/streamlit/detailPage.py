import streamlit as st
import pandas as pd
import os
import requests


@st.cache_data
def load_data():
    columns = [
        "ID", "Name", "Height_m", "Weight_kg",
        "HP", "Attack", "Defense", "Sp_Atk", "Sp_Def", "Speed",
        "Type_1", "Type_2",
        "isLegendary", "isMythical",
        "EggGroup_1", "EggGroup_2",
        "Generation", "CatchRate", "BaseFriendship",
        "isBaby", "EvoStages", "PrevEvolution", "hasGenderDiff",
        "BaseTotal"
    ]
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir,
                            "../../machine_learning/resources/pokemon-dataset-gen-1-9/versions/10/pokemondataset_updated.csv")
    df = pd.read_csv(csv_path, header=None, names=columns)
    df["Type_2"] = df["Type_2"].fillna("")
    return df



st.set_page_config(
    page_title="Pokemon Detail",
    layout="centered"
)

df = load_data()

st.title("Pokemon Detail")

pokemon_names = df["Name"].tolist()
selected_name = st.selectbox("Choose your pokémon", pokemon_names)
res=requests.get(f'http://127.0.0.1:8000/getSpecificPokemon/{selected_name}')

pokemon = df[df["Name"] == selected_name].iloc[0]

pokemon_id = int(pokemon["ID"])
image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_id}.png"

st.image(image_url, width=150, caption=selected_name)

st.header(pokemon["Name"])
type_str = pokemon["Type_1"]
if pokemon["Type_2"]:
    type_str += f" / {pokemon['Type_2']}"
st.write(f"**Type:** {type_str}")

st.write(f"**Generation:** {pokemon['Generation']}")

if pokemon["isLegendary"]:
    st.write("Legendary")
if pokemon["isMythical"]:
    st.write("Mythical")

st.divider()

st.subheader("Base Stats")

stats = {
    "HP": int(pokemon["HP"]),
    "Attack": int(pokemon["Attack"]),
    "Defense": int(pokemon["Defense"]),
    "Sp. Atk": int(pokemon["Sp_Atk"]),
    "Sp. Def": int(pokemon["Sp_Def"]),
    "Speed": int(pokemon["Speed"]),
}

for stat_name, stat_value in stats.items():
    col1, col2 = st.columns([1, 3])
    col1.write(f"**{stat_name}**")
    col2.progress(stat_value / 255, text=str(stat_value))

st.divider()

st.subheader("Info")
col1, col2 = st.columns(2)
col1.metric("Height", f"{pokemon['Height_m']} m")
col2.metric("Weight", f"{pokemon['Weight_kg']} kg")
col1.metric("Base Stats", int(pokemon["BaseTotal"]))
col2.metric("Catch Rate", int(pokemon["CatchRate"]))