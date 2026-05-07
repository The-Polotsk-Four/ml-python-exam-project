import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


STATS = ['HP', 'Attack', 'Defense', 'Sp.Atk', 'Sp.Def', 'Speed']

CLUSTER_COLORS = [
    '#e63946', '#2a9d8f', '#f4a261', '#457b9d',
    '#8ecae6', '#a8dadc', '#606c38', '#e9c46a',
    '#264653', '#f77f00',
]

# ── page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title='Pokemon Cluster',
    layout='wide',
)

# ── custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap');

  html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
  }
  h1, h2, h3 {
    font-family: 'Space Mono', monospace !important;
  }
  .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
  }
  .metric-card {
    background: #1a1a2e;
    border: 1px solid #2d2d4e;
    border-radius: 8px;
    padding: 1rem 1.25rem;
  }
  .stDataFrame {
    border: 1px solid #2d2d4e;
    border-radius: 8px;
  }
  section[data-testid="stSidebar"] {
    background: #0f0f1a;
    border-right: 1px solid #2d2d4e;
  }
  .stSelectbox label, .stSlider label, .stFileUploader label {
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: #a0a0c0;
  }
</style>
""", unsafe_allow_html=True)


# ── helpers ───────────────────────────────────────────────────────────────────
DATA_PATH = '../../machine_learning/resources/pokemon-dataset-gen-1-9/versions/10/pokemondataset_updated.csv'


# loads the pokemon dataset
@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)



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


def make_radar_fig(df: pd.DataFrame, k: int):
    fig = go.Figure()
    for i in range(k):
        cluster_df = df[df['cluster'] == str(i)]
        means = cluster_df[STATS].mean().values.tolist()
        means += means[:1]  
        fig.add_trace(go.Scatterpolar(
            r=means,
            theta=STATS + [STATS[0]],
            fill='toself',
            name=f'Cluster {i}',
            line=dict(color=CLUSTER_COLORS[i % len(CLUSTER_COLORS)]),
            fillcolor=CLUSTER_COLORS[i % len(CLUSTER_COLORS)],
            opacity=0.25,
        ))
    fig.update_layout(
        polar=dict(
            bgcolor='#0f0f1a',
            radialaxis=dict(visible=True, color='#555577'),
            angularaxis=dict(color='#555577'),
        ),
        title=dict(text='Cluster Stat Profiles', font=dict(family='Space Mono', size=13)),
        plot_bgcolor='#0f0f1a',
        paper_bgcolor='#0f0f1a',
        font=dict(color='#c0c0d8'),
        margin=dict(l=40, r=40, t=50, b=40),
    )
    return fig


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


# ── sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## Pokemon\nCluster Lab")
    st.divider()

    st.markdown('#### K_means elbow test')
    k_max = st.slider('Max k to test', 3, 15, 10)

    st.divider()
    st.markdown('#### Clustering')
    k_final = st.slider('Number of clusters (k)', 2, k_max, 3)

    st.divider()
    st.markdown('#### Distribution')
    stat_choice = st.selectbox('Stat for box plot', STATS)


# ── main ──────────────────────────────────────────────────────────────────────
st.markdown("# Pokemon Cluster")

try:
    df_raw = load_data()
except FileNotFoundError:
    st.error(f'Dataset not found at: `{DATA_PATH}`')
    st.stop()

missing = [c for c in STATS if c not in df_raw.columns]
if missing:
    st.error(f'Missing columns: {missing}')
    st.stop()


# ── elbow ─────────────────────────────────────────────────────────────────────
with st.spinner('Computing elbow curve...'):
    elbow = compute_elbow(df_raw, k_max)

# ── clustering ────────────────────────────────────────────────────────────────
with st.spinner('Running k-means...'):
    df_clustered = run_clustering(df_raw, k_final)

# ── summary metrics ───────────────────────────────────────────────────────────
col_a, col_b, col_c, col_d = st.columns(4)
col_a.metric('Pokemon', len(df_clustered))
col_b.metric('Clusters', k_final)
col_c.metric('Inertia', f"{elbow['inertias'][k_final - 2]:,.0f}")
col_d.metric('Avg cluster size', f"{len(df_clustered) // k_final}")

st.divider()

st.plotly_chart(make_scatter_fig(df_clustered, k_final), use_container_width=True)



# ── charts row 1 ─────────────────────────────────────────────────────────────
c1, c2 = st.columns(2)
with c1:
    st.plotly_chart(make_box_fig(df_clustered, stat_choice, k_final), use_container_width=True)
with c2:
    st.plotly_chart(make_elbow_fig(elbow), use_container_width=True)

# ── charts row 2 ─────────────────────────────────────────────────────────────
# c3, c4 = st.columns(2)
# with c3:
#     st.plotly_chart(make_radar_fig(df_clustered, k_final), use_container_width=True)
# with c4:
#     st.plotly_chart(make_box_fig(df_clustered, stat_choice, k_final), use_container_width=True)
# st.plotly_chart(make_box_fig(df_clustered, stat_choice, k_final), use_container_width=True)



# ── cluster summary table ─────────────────────────────────────────────────────
st.divider()
st.markdown('### Cluster Summary')
summary = (
    df_clustered.groupby('cluster')[STATS]
    .agg(['mean', 'std', 'count'])
    .round(1)
)
st.dataframe(summary, use_container_width=True)

# ── raw data ──────────────────────────────────────────────────────────────────
with st.expander('Raw clustered data'):
    display_cols = ['cluster', 'pca1', 'pca2'] + STATS
    if 'Name' in df_clustered.columns:
        display_cols = ['Name'] + display_cols
    st.dataframe(df_clustered[display_cols], use_container_width=True)

    csv = df_clustered.to_csv(index=False).encode('utf-8')
    st.download_button('Download clustered CSV', csv, 'pokemon_clustered.csv', 'text/csv')