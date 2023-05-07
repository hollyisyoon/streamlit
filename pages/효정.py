import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

import koreanize_matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.colors import to_rgba
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import ast
import time

import streamlit as st
from streamlit_extras.let_it_rain import rain
from streamlit_tags import st_tags

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from collections import Counter
from wordcloud import WordCloud
from datetime import datetime, timedelta

import warnings
warnings.filterwarnings("ignore", message="PyplotGlobalUseWarning")
import networkx as nx
from gensim.models import Word2Vec
import time
import itertools
from markdownlit import mdlit

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

try :
    st.markdown(f"<style>{STYLE}</style>", unsafe_allow_html=True)
    st.markdown("<h3>키워드별 영향도 그래프</h3>", unsafe_allow_html=True)
    deepdive_df, deepdive_keywords = get_df(df2, keyword1, keyword2)
    deepdive_lineplot(deepdive_df, deepdive_keywords)

    this_week_words = list(이번주_df['unique_content'].explode())
    last_week_words = list(지난주_df['unique_content'].explode())

    this_week_word_counts = Counter(this_week_words)
    last_week_word_counts = Counter(last_week_words)

    # 이번주와 지난주에 모두 언급된 단어를 모은 집합
    common_words = set(this_week_word_counts.keys()) & set(last_week_word_counts.keys())
    result = {}
    for word in common_words:
        # 해당 단어가 언급된 모든 URL을 리스트로 모음
        url_list = list(이번주_df.loc[이번주_df['unique_content'].apply(lambda x: word in x)]['URL'])
        # 영향도가 가장 높은 URL을 찾아서 출력
        url = max(url_list, key=lambda x: 이번주_df.loc[이번주_df['URL'] == x, '영향도'].iloc[0])
        increase_rate = (this_week_word_counts[word] - last_week_word_counts[word]) / this_week_word_counts[word]
        result[word] = {'상승률': round(increase_rate, 2), 'URL': url}

    # 상승률 기준 상위 10개 단어 출력
    keywords = []
    ups = []
    urls = []
    title = []

    for word, data in sorted(result.items(), key=lambda x: x[1]['상승률'], reverse=True):
        if data['상승률']>0:
            keywords.append(word)
            ups.append(f"{data['상승률']*100}%")
            urls.append(data['URL'])
            
    result_df = pd.DataFrame({
        '키워드': keywords,
        '상승률': ups,
        'URL': urls
    })

    if len(result_df.index) >= 1 :
        return result_df
    
st.subheader('🔥 급상승 키워드')
try:
    rising_keyword = rising_keyword(standard_df, new_df)
    rising_keyword
except:
    st.warning("⚠️ 해당 기간 동안 급상승 키워드가 존재하지 않습니다")