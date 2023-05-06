import pandas as pd

#시각화
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

rain(emoji="🌼",
    font_size=54,
    falling_speed=5,
    animation_length="infinite")

######데이터#########
def to_list(text):
    return ast.literal_eval(text)

df = pd.read_csv('/app/streamlit/data/df_트렌드_github.csv')
df['날짜'] = pd.to_datetime(df['날짜'])

st.title('🔎 키워드 DeepDive')
col1, col2 = st.beta_columns((0.2, 0.8))
keyword1 = st.text_input('궁금한 키워드', value='해충제')
keyword2 = st_tags(
    label = '비교할 키워드',
    text = '직접 입력해보세요(최대 5개)',
    value = ['식물영양제', '뿌리영양제'],
    suggestions = ['해충제', '제라늄'],
    maxtags = 5,
    key = '1')

def get_df(df, word1, args):
    # word1 은 반드시 입력해야 하는 기준
    # 입력한 단어 중 하나 이상이 포함된 행 찾기
    df['날짜'] = pd.to_datetime(df['날짜'])
    result = df[(df['매체'] == '식물갤러리') | (df['매체'] == '식물병원')]
    result = result[(result['날짜'] >= '2022-04-27') & (result['날짜'] <= '2023-04-26')]
    keywords = [word1] + (args)
    result = result[result['제목+내용(nng)'].str.contains('|'.join(keywords))]
    return result

hello = get_df(df, keyword1, keyword2)
hello