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


st.title("Yellow component")

html_content = "<div>Hello world</div>"
yellow_background = "<style>:root {background-color: yellow;}</style>"
components.html(yellow_background + html_content)

df = pd.read_csv('/app/streamlit/data/df_트렌드_github.csv')
df['날짜'] = pd.to_datetime(df['날짜'])
# df['제목+내용(nng)'] = df['제목+내용(nng)'].map(to_list)

def extract_df(df, media, start_date, end_date, effect_size):
    start_date = pd.Timestamp(start_date)
    end_date = pd.Timestamp(end_date)
    standard_df = df[(df['매체'] == media) & (df['날짜'] >= start_date) & (df['날짜'] <= end_date) & (df['영향도'] >= effect_size)]
    range_days = (end_date - start_date) + timedelta(days = 1)
    new_day = start_date - range_days
    new_day = pd.Timestamp(new_day)
    new_df = df[(df['매체'] == media) & (df['날짜'] >= new_day) & (df['날짜'] < start_date) & (df['영향도'] >= effect_size)]
    return standard_df, new_df

col1, col2, col3 = st.beta_columns(3)

min_date = datetime(2022, 6, 1)
max_date = datetime(2023, 4, 26)
with col1:
    start_date = st.date_input("시작 날짜",
                               value=datetime(2022,6,1),
                               min_value=min_date,
                               max_value=max_date - timedelta(days=7))
    # 끝 날짜를 선택할 때 최소 날짜는 시작 날짜이며, 최대 날짜는 90일 이전까지로 제한
    end_date = st.date_input("끝 날짜",
                             value=datetime(2022,6,15),
                             min_value=start_date + timedelta(days=7),
                             max_value=start_date + timedelta(days=60))

with col2:
    media = st.selectbox('매체',('식물갤러리', '식물병원', '네이버카페', '네이버블로그', '네이버포스트'))

with col3:
    temp_effect_size = st.slider('영향도 볼륨', 0, 100, 80)
    effect_size = (100-int(temp_effect_size))/100

standard_df, new_df = extract_df(df, media, start_date, end_date, effect_size)

def rising_keyword(standard_df, new_df):
    # 데이터 합치기 
    df = pd.concat([standard_df, new_df])

    # 날짜 구하기
    이번주마지막날 = df['날짜'].max()
    이번주첫날 = (df['날짜'].max() - timedelta(days=7))
    지난주첫날 = 이번주첫날 - timedelta(days=7)
    
    이번주_df = df[(df['날짜'] > 이번주첫날) & (df['날짜'] <= 이번주마지막날)]
    지난주_df = df[(df['날짜'] > 지난주첫날) & (df['날짜'] <= 이번주첫날)]
        
    # 중복값 제거한 새로운 열 추가
    이번주_df = 이번주_df.copy()
    이번주_df['unique_content'] = 이번주_df['제목+내용(nng)'].apply(lambda x: ast.literal_eval(x))
    이번주_df['unique_content'] = 이번주_df['unique_content'].apply(lambda x: list(set(x)))

    지난주_df = 지난주_df.copy()
    지난주_df['unique_content'] = 지난주_df['제목+내용(nng)'].apply(lambda x: ast.literal_eval(x))
    지난주_df['unique_content'] = 지난주_df['unique_content'].apply(lambda x: list(set(x)))

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
    titles = []

    for word, data in sorted(result.items(), key=lambda x: x[1]['상승률'], reverse=True):
        if data['상승률']>0:
            keywords.append(word)
            ups.append(f"{data['상승률']*100}%")
            urls.append(data['URL'])
            titles.append(data['제목'])

    result_df = pd.DataFrame({
        '키워드': keywords,
        '상승률': ups,
        'URL': urls,
        'title': titles
    })

    if len(result_df.index) >= 1 :
        return result_df
    
st.subheader('🔥 급상승 키워드')
try:
    rising_keyword = rising_keyword(standard_df, new_df)
    rising_keyword
except:
    st.warning("⚠️ 해당 기간 동안 급상승 키워드가 존재하지 않습니다")