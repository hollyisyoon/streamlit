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

css_code = """
<style>
    .custom-sidebar {
        padding: 20px;
        background-color: #f2f2f2;
        font-size: 18px;
        color: #333;
    }
    
    .custom-sidebar a {
        color: #333;
        text-decoration: none;
    }
</style>
"""

STYLE = """
.callout {
    padding: 1em;
    border-radius: 0.5em;
    background-color: #F8F8F8;
    border-left: 4px solid #195ef7;
    margin-bottom: 1em;
    color: black;
}

.callout a#key1 {
    color: #000;
    background-color: #FAF3DD;
    text-decoration: none;
}

.callout a#key2 {
    color: #000;
    background-color: #E9F3F7;
    text-decoration: none;
}

.callout a#key3 {
    color: #000;
    background-color: #F6F3F8;
    text-decoration: none;
}

.callout a#key4 {
    color: #000;
    background-color: #EEF3ED;
    text-decoration: none;
}
"""

df = pd.read_csv('/app/streamlit/data/df_트렌드_github.csv')
df['날짜'] = pd.to_datetime(df['날짜'])
st.title('🔎 키워드 DeepDive')

#########Section3 - 키워드 deepdive(시계열)############
col1, col2 = st.beta_columns((0.3, 0.7))
with col1:
    keyword1 = st.text_input('궁금한 키워드', value='제라늄')
with col2:
    keyword2 = st_tags(
        label = '비교할 키워드',
        text = '직접 입력해보세요(최대 5개)',
        value = ['총채벌레','뿌리파리'],
        maxtags = 5,
        key = '2')

def get_df(df, word1, args):
    result = df[(df['매체'] == '식물갤러리') | (df['매체'] == '식물병원')]
    result = result[(result['날짜'] >= '2022-04-27') & (result['날짜'] <= '2023-04-26')]
    keywords = [word1] + (args)
    result = result[result['제목+내용(nng)'].str.contains('|'.join(keywords))]
    for arg in keywords:
        if arg not in ' '.join(result['제목+내용(nng)'].tolist()):
            st.warning(f"'다음 언급되지 않은 키워드입니다. 다시 입력해주세요. {arg}'")
            return None, None
    return result, keywords

def deepdive_lineplot(df, keywords):
    # 키워드별로 데이터프레임을 분리합니다.
    keywords = keywords[::-1]
    keyword_dfs = {}
    for keyword in keywords:
        keyword_dfs[keyword] = df[df['제목+내용(nng)'].str.contains(keyword)].copy()

    # 날짜별로 그룹핑하고 영향도 평균을 구합니다.
    impact_by_week = {}
    for keyword, keyword_df in keyword_dfs.items():
        keyword_df['날짜'] = pd.to_datetime(keyword_df['날짜'])
        keyword_df.set_index('날짜', inplace=True)
        impact_by_week[keyword] = keyword_df.resample('W')['영향도'].mean()

    # 라인 그래프를 그립니다.
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # 첫 번째 키워드는 파란색으로, 나머지는 회색으로 처리합니다.
    colors = ["grey"] * (len(keywords) - 1) + ["blue"]

    for i, (keyword, impact) in enumerate(impact_by_week.items()):
        fig.add_trace(go.Scatter(x=impact.index, y=impact.values, name=keyword, line_color=colors[i]), secondary_y=False)
        
    fig.update_layout(yaxis_title="평균 영향도")
    st.plotly_chart(fig, use_container_width=True)


deepdive_df, deepdive_keywords = get_df(df, keyword1, keyword2)
deepdive_lineplot(deepdive_df, deepdive_keywords)

# except :
#     st.warning("해당 키워드에 대한 결과가 존재하지 않습니다")

#########Section4 - 키워드 deepdive(네트워크 분석)############
st.markdown("---")
st.markdown("<h2 id='section4'>키워드 연관탐색</h2>", unsafe_allow_html=True)

all_keywords = [keyword1]+keyword2
st.text(f'🔮 {all_keywords}에 대한 연관분석을 시작합니다')

expander = st.expander('연관분석 세부필터')
with expander:
    media = st.selectbox('매체',('식물갤러리', '식물병원', '네이버카페', '네이버블로그', '네이버포스트'), help="확인하고 싶은 외부 데이터의 매체를 선택할 수 있습니다.")

def extract_df(df, media):
    standard_df = df[(df['매체'] == media)]
    return standard_df

df2 = extract_df(df, media)
network_list = [eval(i) for i in df2['제목+내용(nng)']]

def 네트워크(network_list, all_keywords):
    networks = []
    for review in network_list:
        network_review = [w for w in review if len(w) > 1]
        networks.append(network_review)

    model = Word2Vec(networks, vector_size=100, window=5, min_count=1, workers=4, epochs=50)

    G = nx.Graph(font_path='/app/streamlit/font/Pretendard-Bold.otf')

    # 중심 노드들을 노드로 추가
    for keyword in all_keywords:
        G.add_node(keyword)
        # 주어진 키워드와 가장 유사한 20개의 단어 추출
        similar_words = model.wv.most_similar(keyword, topn=15)
        # 유사한 단어들을 노드로 추가하고, 주어진 키워드와의 연결선 추가
        for word, score in similar_words:
            G.add_node(word)
            G.add_edge(keyword, word, weight=score)
            
    # 노드 크기 결정
    size_dict = nx.degree_centrality(G)

    # 노드 크기 설정
    node_size = []
    for node in G.nodes():
        if node in all_keywords:
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
    pos = nx.spring_layout(G, seed=42, k=0.15)
    nx.draw(G, pos, with_labels=True, node_size=node_size, node_color=node_colors, alpha=0.8, linewidths=1,
            font_size=9, font_color="black", edge_color="grey", width=edge_weights)

    net = Network(notebook=True, cdn_resources='in_line')
    net.from_nx(G)
    return [net, similar_words]

네트워크 = 네트워크(network_list, all_keywords)
if st.button('분석을 시작하기'):
    with st.spinner('분석 중입니다...'):
        try:
            net = 네트워크[0]
            net.save_graph(f'/app/streamlit/pyvis_graph.html')
            HtmlFile = open(f'/app/streamlit/pyvis_graph.html', 'r', encoding='utf-8')
            components.html(HtmlFile.read(), height=600)
        except:
            st.warning('존재하지 않는 키워드예요.')