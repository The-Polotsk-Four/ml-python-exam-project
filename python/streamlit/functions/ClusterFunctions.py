import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# the columns we extract from the dataset and use for the clustering
STATS = ['HP', 'Attack', 'Defense', 'Sp.Atk', 'Sp.Def', 'Speed']

# colors for our cluster
CLUSTER_COLORS = [
    '#e63946', '#2a9d8f', '#f4a261', '#457b9d',
    '#8ecae6', '#a8dadc', '#606c38', '#e9c46a',
    '#264653', '#f77f00',
]

# path to our csv file
DATA_PATH = 'machine_learning/resources/pokemon-dataset-gen-1-9/versions/10/pokemondataset_updated.csv'


# loads the pokemon dataset
@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)


# st.cache_data is used to cache the data in our browser

# computes the elbow diagram with from the raw dataset
@st.cache_data
def compute_elbow(_df: pd.DataFrame, k_max: int):
    X = _df[STATS].dropna().values
    k_range = range(2, k_max + 1)
    inertias = []
    for k in k_range:
        km = KMeans(n_clusters=k, 
                    random_state=42, 
                    n_init=5, 
                    max_iter=300, 
                    algorithm='lloyd')
        km.fit(X)
        inertias.append(km.inertia_)
    return {'k_range': list(k_range), 'inertias': inertias}

# creates the elbow fig with the data from the the compute_elbow function
def make_elbow_fig(elbow: dict):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=elbow['k_range'],
        y=elbow['inertias'],
        mode='lines+markers',
        line=dict(color='#e63946', width=2),
        marker=dict(size=7, color='#e63946'),
        name='Inertia',
    ))
    fig.update_layout(
        title=dict(text='Elbow Curve', font=dict(family='Space Mono', size=13)),
        xaxis=dict(title='k (clusters)', tickmode='linear'),
        yaxis=dict(title='Inertia'),
        plot_bgcolor='#0f0f1a',
        paper_bgcolor='#0f0f1a',
        font=dict(color='#c0c0d8'),
        margin=dict(l=40, r=20, t=40, b=40),
    )
    return fig


# creates the clustering with the data from our dataset  
# using the K value we have defined
@st.cache_data
def run_clustering(_df: pd.DataFrame, k: int):
    X = _df[STATS].dropna().values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)
    pca = PCA(n_components=2, random_state=42)
    X_pca = pca.fit_transform(X_scaled)
    df_out = _df.dropna(subset=STATS).copy()
    df_out['cluster'] = clusters.astype(str)
    df_out['pca1'] = X_pca[:, 0]
    df_out['pca2'] = X_pca[:, 1]
    return df_out

# creates the fig so we can see the results in a diagram
def make_scatter_fig(df: pd.DataFrame, k: int):
    hover_cols = ['Name', 'cluster',] + STATS + ['Total_Stats'] if 'Name' in df.columns else ['cluster'] + STATS
    color_map = {str(i): CLUSTER_COLORS[i % len(CLUSTER_COLORS)] for i in range(k)}

    fig = px.scatter(
        df,
        x='pca1',
        y='pca2',
        color='cluster',
        hover_data={c: True for c in hover_cols},
        color_discrete_map=color_map,
        opacity=0.82,
    )
    fig.update_traces(marker=dict(size=6))
    fig.update_layout(
        title=dict(text='Cluster', font=dict(family='Space Mono', size=13)),
        xaxis=dict(title='PC 1'),
        yaxis=dict(title='PC 2'),
        plot_bgcolor='#0f0f1a',
        paper_bgcolor='#0f0f1a',
        font=dict(color='#c0c0d8'),
        legend=dict(title='Cluster'),
        margin=dict(l=40, r=20, t=40, b=40),
    )
    return fig

# creates a box fig with the data from dataset using the chosen stat and k_means
def make_box_fig(df: pd.DataFrame, stat: str, k: int):
    color_map = {str(i): CLUSTER_COLORS[i % len(CLUSTER_COLORS)] for i in range(k)}
    fig = px.box(
        df, x='cluster', y=stat,
        color='cluster',
        color_discrete_map=color_map,
        points='outliers',
    )
    fig.update_layout(
        title=dict(text=f'{stat} Boxplot', font=dict(family='Space Mono', size=13)),
        showlegend=False,
        plot_bgcolor='#0f0f1a',
        paper_bgcolor='#0f0f1a',
        font=dict(color='#c0c0d8'),
        margin=dict(l=40, r=20, t=40, b=40),
    )
    return fig