import streamlit as st
from gensim.models import Word2Vec
import networkx as nx
from pyvis.network import Network
import gensim
from wordcloud import WordCloud
from datetime import datetime, timedelta
import pandas as pd
from streamlit_tags import st_tags

df = pd.read_csv('/app/streamlit/data/df_트렌드_github.csv')

st.title('🔎 키워드 DeepDive')
col1, col2 = st.beta_columns((0.2, 0.8))
keyword1 = st.text_input('궁금한 키워드', value='제라늄')
keyword2 = st_tags(
    label = '비교할 키워드',
    text = '직접 입력해보세요(최대 5개)',
    value = ['식물영양제', '뿌리영양제'],
    maxtags = 5,
    key = '2')

keyword_all = [keyword1]+keyword2
network_keywords = [keyword.split() for keyword in df['제목+내용(nng)']]

def 네트워크(network_keywords):
    networks = []
    for keyword in network_keywords:
        network_keyword = [w for w in keyword if len(w) > 1]
        networks.append(network_keyword)

    model = Word2Vec(networks, vector_size=100, window=5, min_count=1, workers=3, epochs=50)

    G = nx.Graph(font_path='/app/streamlit/font/Pretendard-Bold.otf')

    # 중심 노드들을 노드로 추가
    for keyword in keyword_all:
        G.add_node(keyword)
        # 주어진 키워드와 가장 유사한 20개의 단어 추출
        similar_words = model.wv.most_similar(keyword, topn=10)
        # 유사한 단어들을 노드로 추가하고, 주어진 키워드와의 연결선 추가
        for word, score in similar_words:
            G.add_node(word)
            G.add_edge(keyword, word, weight=score)
            
    # 노드 크기 결정
    size_dict = nx.degree_centrality(G)

    # 노드 크기 설정
    node_size = []
    for node in G.nodes():
        if node in keyword_all:
            node_size.append(5000)
        else:
            node_size.append(1000)

    # 클러스터링
    clusters = list(nx.algorithms.community.greedy_modularity_communities(G))
    cluster_labels = {}
    for i, cluster in enumerate(clusters):
        for node in cluster:
            cluster_labels[node] = i
            
    # 노드 색상 결정
    color_palette = ["#f39c9c", "#f7b977", "#fff4c4", "#d8f4b9", "#9ed6b5", "#9ce8f4", "#a1a4f4", "#e4b8f9", "#f4a2e6", "#c2c2c2"]
    node_colors = [color_palette[cluster_labels[node] % len(color_palette)] for node in G.nodes()]

    # 노드에 라벨과 연결 강도 값 추가
    edge_weights = [d['weight'] for u, v, d in G.edges(data=True)]

    # 선의 길이를 변경 pos
    # plt.figure(figsize=(15,15))
    pos = nx.spring_layout(G, seed=42, k=0.15)
    nx.draw(G, pos, font_path='/app/streamlit/font/Pretendard-Bold.otf', with_labels=True, node_size=node_size, node_color=node_colors, alpha=0.8, linewidths=1,
            font_size=9, font_color="black", font_weight="medium", edge_color="grey", width=edge_weights)


    # 중심 노드들끼리 겹치는 단어 출력
    overlapping_키워드 = set()
    for i, keyword1 in enumerate(키워드):
        for j, keyword2 in enumerate(키워드):
            if i < j and keyword1 in G and keyword2 in G:
                if nx.has_path(G, keyword1, keyword2):
                    overlapping_키워드.add(keyword1)
                    overlapping_키워드.add(keyword2)
    if overlapping_키워드:
        print(f"다음 중심 키워드들끼리 연관성이 있어 중복될 가능성이 있습니다: {', '.join(overlapping_키워드)}")


    net = Network(notebook=True, cdn_resources='in_line')
    net.from_nx(G)
    return [net, similar_words]

network_result = 네트워크(network_keywords)

try:
    net = network_result[0]
    net.save_graph(f'/app/streamlit/pyvis_graph.html')
    HtmlFile = open(f'/app/streamlit/pyvis_graph.html', 'r', encoding='utf-8')
    components.html(HtmlFile.read())
except:
    st.write('존재하지 않는 키워드예요.')