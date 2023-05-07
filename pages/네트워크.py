import streamlit as st
import streamlit.components.v1 as components
from streamlit_tags import st_tags

import plotly.express as px
import plotly.graph_objects as go

# 기본 라이브러리
import os
import ast
from datetime import datetime
from datetime import timedelta

import warnings
warnings.filterwarnings("ignore", message="PyplotGlobalUseWarning")

from collections import Counter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib

from PIL import Image

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

from gensim.models import Word2Vec
import networkx as nx
import gensim
from pyvis.network import Network
from wordcloud import WordCloud

df = pd.read_csv('/app/streamlit/data/df_트렌드_github.csv')

st.title('🔎 키워드 DeepDive')
col1, col2 = st.beta_columns((0.2, 0.8))
keyword1 = st.text_input('궁금한 키워드', value='제라늄')
keyword2 = st_tags(
    label = '비교할 키워드',
    text = '직접 입력해보세요(최대 5개)',
    value = ['스킨답서스'],
    maxtags = 5,
    key = '2')

all_keywords = [keyword1]+keyword2
network_list = [eval(i) for i in df['제목+내용(nng)']]

def create_network(network_list, all_keywords):
    networks = []
    for review in network_list:
        network_review = [w for w in review if len(w) > 1]
        networks.append(network_review)

    model = Word2Vec(networks, vector_size=100, window=5, min_count=1, workers=3, epochs=50)

    G = nx.Graph(font_path='/app/streamlit/font/Pretendard-Bold.otf')

    # Add central nodes
    for keyword in all_keywords:
        G.add_node(keyword)
        similar_words = model.wv.most_similar(keyword, topn=20)
        for word, score in similar_words:
            G.add_node(word)
            G.add_edge(keyword, word, weight=score)

    # Determine node sizes
    node_size = [5000 if node in all_keywords else 1000 for node in G.nodes()]

    # Cluster nodes
    clusters = list(nx.algorithms.community.greedy_modularity_communities(G))
    cluster_labels = {}
    for i, cluster in enumerate(clusters):
        for node in cluster:
            cluster_labels[node] = i

    # Determine node colors
    color_palette = ["#f39c9c", "#f7b977", "#fff4c4", "#d8f4b9", "#9ed6b5", "#9ce8f4", "#a1a4f4", "#e4b8f9", "#f4a2e6", "#c2c2c2"]
    node_colors = [color_palette[cluster_labels[node] % len(color_palette)] for node in G.nodes()]

    # Determine edge weights
    edge_weights = [d["weight"] for _, _, d in G.edges(data=True)]

    # Create the graph visualization
    net = Network(height="500px", width="100%", font_color="black")
    net.from_nx(G)
    net.options.update(
        {
            "nodes": {
                "shape": "dot",
                "size": node_size,
                "color": node_colors,
                "font": {
                    "size": 9,
                    "color": "black",
                },
            },
            "edges": {
                "color": "grey",
                "width": edge_weights,
            },
            "physics": {
                "forceAtlas2Based": {
                    "gravitationalConstant": -50,
                    "centralGravity": 0.05,
                    "springLength": 100,
                    "springConstant": 0.2,
                },
                "minVelocity": 0.75,
            },
        }
    )
    return net, node_size, node_colors, edge_weights

net, node_size, node_colors, edge_weights = create_network(network_list, all_keywords)
net.show_buttons(filter_=["physics"])
net.save_graph("/app/streamlit/pyvis_graph.html")

# Call the function to create the network
create_network(network_list, all_keywords)

# Display the graph in Streamlit
try:
    HtmlFile = open("/app/streamlit/pyvis_graph.html", "r", encoding="utf-8")
    components.html(HtmlFile.read())
except:
    st.warning("존재하지 않는 키워드예요.")
