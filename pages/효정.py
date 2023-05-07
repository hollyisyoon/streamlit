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

    # 전체 기간을 기준으로 주차 단위로 resampling 하기 위해
    # 날짜 범위를 생성합니다.
    date_range = pd.date_range(start=df['날짜'].min(), end=df['날짜'].max(), freq='W')

    # 날짜별로 그룹핑하고 영향도 평균을 구합니다.
    impact_by_week = {}
    for keyword, keyword_df in keyword_dfs.items():
        keyword_df['날짜'] = pd.to_datetime(keyword_df['날짜'])
        keyword_df.set_index('날짜', inplace=True)
        impact_by_week[keyword] = keyword_df.resample('W')['영향도'].mean()

    # 각 키워드별로 인덱스를 맞추어주고, 데이터가 없는 부분은 보간하여 채워줍니다.
    for keyword in keywords:
        impact = impact_by_week[keyword].reindex(date_range, fill_value=pd.NaT)
        impact_by_week[keyword] = impact.interpolate()

    # 라인 그래프를 그립니다.
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # 첫 번째 키워드는 파란색으로, 나머지는 회색으로 처리합니다.
    colors = ["grey"] * (len(keywords) - 1) + ["blue"]


    for i, (keyword, impact) in enumerate(impact_by_week.items()):
        # 영향도 데이터를 보간합니다.
        impact = impact.interpolate()
        fig.add_trace(
            go.Scatter(
                x=impact.index,
                y=impact.values,
                name=keyword,
                line_color=colors[i],
                line_dash='dot' if i < len(keywords) - 1 else None  # 회색 라인을 점선으로 변경
            ),
            secondary_y=False
        )
         fig.add_trace(
            go.Scatter(
                x=impact.index,
                y=impact.values,
                name=keyword,
                line_color=colors[i],
                line_dash='dot' if i < len(keywords) - 1 else 'solid'  # 회색 라인을 점선으로 변경
            ),
            secondary_y=False
        )
       
        
    fig.update_layout(yaxis_title="평균 영향도")
    st.plotly_chart(fig, use_container_width=True)

try :
    deepdive_df, deepdive_keywords = get_df(df2, keyword1, keyword2)
    deepdive_lineplot(deepdive_df, deepdive_keywords)

except :
    st.warning("해당 키워드에 대한 결과가 존재하지 않습니다")