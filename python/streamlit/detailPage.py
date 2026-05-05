import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from PIL import Image


st.set_page_config(
    page_title='DetailPage',
    layout='centered'
)

TYPE_COLORS = {
    "Fire": "#E25822", "Grass": "#3B8A2A", "Water": "#2980B9",
    "Electric": "#F0C040", "Psychic": "#C0306A", "Ice": "#6BC4D4",
    "Dragon": "#5B3EC8", "Dark": "#4A3B30", "Fairy": "#C9699E",
    "Normal": "#9A9977", "Fighting": "#B83030", "Flying": "#6D90C4",
    "Poison": "#7B3FA0", "Ground": "#C4A63C", "Rock": "#A09060",
    "Bug": "#829620", "Ghost": "#5A4070", "Steel": "#9BA0A8",
}

STAT_COLORS = {
    'HP': '#E25822',
    'Attack': '#E24B4A',
    'Defense': '#378ADD',
    'Sp. Atk': '#9B59B6',
    'Sp Def': '#1D9E75',
    'Speed': '#F0C040',
}

st.markdown("""
<style>
.type-badge {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
    color: white;
    margin-right: 6px;
}
.stat-label {
    font-size: 13px;
    color: #888;
    width: 70px;
    display: inline-block;
    text-align: right;
    margin-right: 8px;
}
.stat-value {
    font-size: 13px;
    font-weight: 600;
    width: 30px;
    display: inline-block;
    text-align: right;
    margin-right: 8px;
}            
.pokemon-name {
    font-size: 2rem;
    font-wight: 700;
    margin: 0;
}
.pokemon-num {
    font-size: 1rem;
    color: #aaa;
}
.info-label {
    font-size: 11px;
    color: #aaa;
    text-transform: uppercase;
    letter-spacing: 0.05px;
}
.info-value {
    font-size: 10px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv('../../machine_learning/resources/pokemon-dataset-get-1-9/versions/10/pokemondataset:updated.csv')
    df =["Type_2"] = df["Type_2"].fillna("")
    return df



st.text('detail page')