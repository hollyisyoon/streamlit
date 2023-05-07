import koreanize_matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.colors import to_rgba
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from pyvis.network import Network
import networkx as nx
import gensim
from gensim.models import Word2Vec
from PIL import Image

import pandas as pd
import ast
import time
from datetime import datetime, timedelta
import itertools
from markdownlit import mdlit

import streamlit as st
from streamlit_extras.let_it_rain import rain
from streamlit_tags import st_tags
import warnings
warnings.filterwarnings("ignore", message="PyplotGlobalUseWarning")

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from collections import Counter
from wordcloud import WordCloud


# CSS 스타일 정의
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

st.title("외부 트렌드 모니터링 대시보드")

#########Section3 - 키워드 deepdive(시계열)############
st.markdown("---")
st.markdown("<h2 id='section3'>⏳ 시기별 키워드 영향도</h2>", unsafe_allow_html=True)
df2 = pd.read_csv('/app/streamlit/data/df_트렌드_github.csv')
df2['날짜'] = pd.to_datetime(df2['날짜'])

col1, col2 = st.beta_columns((0.2, 0.8))
with col1:
    keyword1 = st.text_input('궁금한 키워드', value='제라늄')
with col2:
    keyword2 = st_tags(
        label = '비교할 키워드',
        text = '직접 입력해보세요(최대 5개)',
        value = ['스킨답서스'],
        maxtags = 5,
        key = '2')

def get_df(df, word1, args):
    df['날짜'] = pd.to_datetime(df['날짜'])
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

def get_TOP_10(df, keyword):
    temp_df = df[df['제목+내용(nng)'].str.contains(keyword)]
    top10_list = []
    for media_category in temp_df['매체'].unique():
        df_category = temp_df[temp_df['매체'] == media_category]
        if len(df_category) > 0:
            try:
                band_top10 = df_category.nlargest(10, '영향도')
                band_top10['영향도'] *= 100  # 영향도를 퍼센트로 변환
                band_top10 = band_top10.reset_index(drop=True)
                band_top10 = band_top10[['매체', '작성자', '제목', 'URL', '영향도']]
                top10_list.append(band_top10)
            except ValueError:
                df_category['영향도'] *= 100  # 영향도를 퍼센트로 변환
                df_category = df_category.reset_index(drop=True)
                df_category = df_category[['매체', '작성자', '제목', 'URL', '영향도']]
                top10_list.append(df_category)
    if len(top10_list) > 0:
        return pd.concat(top10_list, ignore_index=False)
    else:
        return None
    
try :
    st.markdown(f"<style>{STYLE}</style>", unsafe_allow_html=True)
    st.markdown("<h3>키워드별 영향도 그래프</h3>", unsafe_allow_html=True)
    deepdive_df, deepdive_keywords = get_df(df2, keyword1, keyword2)
    deepdive_lineplot(deepdive_df, deepdive_keywords)
    st.markdown("<h3>매체별 Top10 게시글</h3>", unsafe_allow_html=True)
    keyword_result = get_TOP_10(df2, keyword1)
    st.dataframe(keyword_result)

except :
    st.warning("해당 키워드에 대한 결과가 존재하지 않습니다")


#########Section4 - 키워드 deepdive(네트워크 분석)############
st.markdown("---")
st.markdown("<h2 id='section4'>키워드 연관탐색</h2>", unsafe_allow_html=True)

all_keywords = [keyword1]+keyword2
st.text(f'🔮 {all_keywords}에 대한 연관분석을 시작합니다')

#네트워크 분석결과
def 네트워크(network_list, all_keywords):
    networks = []
    for review in network_list:
        network_review = [w for w in review if len(w) > 1]
        networks.append(network_review)

    model = Word2Vec(networks, vector_size=100, window=5, min_count=1, workers=4, epochs=100)

    G = nx.Graph(font_path='/app/streamlit/font/NanumBarunGothic.ttf')

    # 중심 노드들을 노드로 추가
    for keyword in all_keywords:
        G.add_node(keyword)
        # 주어진 키워드와 가장 유사한 20개의 단어 추출
        similar_words = model.wv.most_similar(keyword, topn=20)
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
    # plt.figure(figsize=(15,15))
    pos = nx.spring_layout(G, seed=42, k=0.15)
    nx.draw(G, pos, with_labels=True, node_size=node_size, node_color=node_colors, alpha=0.8, linewidths=1,
            font_size=9, font_color="black", font_weight="medium", edge_color="grey", width=edge_weights)

    # # 중심 노드들끼리 겹치는 단어 출력
    # overlapping_키워드 = set()
    # for i, keyword1 in enumerate(all_keywords):
    #     for j, keyword2 in enumerate(all_keywords):
    #         if i < j and keyword1 in G and keyword2 in G:
    #             if nx.has_path(G, keyword1, keyword2):
    #                 overlapping_키워드.add(keyword1)
    #                 overlapping_키워드.add(keyword2)
    # if overlapping_키워드:
    #     print(f"다음 중심 키워드들끼리 연관성이 있어 중복될 가능성이 있습니다: {', '.join(overlapping_키워드)}")

    net = Network(notebook=True, cdn_resources='in_line')
    net.from_nx(G)
    return [net, similar_words]

#연관분석
expander = st.expander('연관분석 세부필터')
with expander:
    col1, col2= st.beta_columns(2)    
    min_date = datetime(2022, 6, 1)
    max_date = datetime(2023, 4, 26)
    with col1:
        start_date = st.date_input("시작 날짜",
                                value=datetime(2022,6,1),
                                min_value=min_date,
                                max_value=max_date - timedelta(days=7))
        # 끝 날짜를 선택할 때 최소 날짜는 시작 날짜이며, 최대 날짜는 90일 이전까지로 제한
        end_date = st.date_input("끝 날짜",
                                value=datetime(2022,7,1),
                                min_value=start_date + timedelta(days=7),
                                max_value=start_date + timedelta(days=60))
    with col2:
        media = st.selectbox('매체',('식물갤러리', '식물병원', '네이버카페', '네이버블로그', '네이버포스트'), help="확인하고 싶은 외부 데이터의 매체를 선택할 수 있습니다.")

def extract_df(df, media, start_date, end_date):
    start_date = pd.Timestamp(start_date)
    end_date = pd.Timestamp(end_date)
    standard_df = df[(df['매체'] == media) & (df['날짜'] >= start_date) & (df['날짜'] <= end_date)]
    return standard_df

df_연관분석 = extract_df(df2, media, start_date, end_date)

if st.button('분석을 시작하기'):
    with st.spinner('분석 중입니다...'):
        test2 = ['제라늄', '해충', '응애']
        test1 = [eval(i) for i in df_연관분석['제목+내용(nng)']]
        try:
            네트워크 = 네트워크(network_list, all_keywords)
            net = 네트워크[0]
            net.save_graph(f'/app/streamlit/pyvis_graph.html')
            HtmlFile = open(f'/app/streamlit/pyvis_graph.html', 'r', encoding='utf-8')
            components.html(HtmlFile.read(), height=600)
        except:
            st.warning('존재하지 않는 키워드예요.')