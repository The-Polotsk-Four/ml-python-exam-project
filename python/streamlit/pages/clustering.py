import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from functions.ClusterFunctions import *

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