import pandas as pd
import koreanize_matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.colors import to_rgba
import plotly.graph_objects as go
import plotly.express as px
import ast
import time

import streamlit as st
from streamlit_extras.let_it_rain import rain

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from collections import Counter
from wordcloud import WordCloud
from datetime import datetime, timedelta

import warnings
warnings.filterwarnings("ignore", message="PyplotGlobalUseWarning")
import networkx as nx
from gensim.models import Word2Vec
import time

rain(emoji="🦝",
    font_size=54,
    falling_speed=10,
    animation_length="infinite")

df = pd.read_csv('/app/streamlit/data/df_트렌드_github.csv', encoding='utf-8')

######################대시보드
st.title('외부 트렌드 모니터링 대시보드')

#### 인풋 필터 #####
col1, col2, col3 = st.beta_columns(3)

min_date = datetime(2022, 7, 25)
max_date = datetime(2023, 4, 26)
with col1:
    start_date = st.date_input("시작 날짜",
                               value=datetime.today() - timedelta(days=45),
                               min_value=min_date,
                               max_value=max_date)
with col2:
    # 끝 날짜를 선택할 때 최소 날짜는 시작 날짜이며, 최대 날짜는 90일 이전까지로 제한
    end_date = st.date_input("끝 날짜",
                             value=datetime.today() - timedelta(days=30),
                             min_value=start_date,
                             max_value=start_date + timedelta(days=90))

with col3:
    keyword_no = st.number_input("📌 키워드", value=50, min_value=1, step=1)

col1, col2, col3 = st.beta_columns(3)    
with col1:
    type = st.selectbox('기준',('상대 빈도(TF-IDF)','단순 빈도(Countvertize)'))
with col2:
    media = st.selectbox('매체',('식물갤러리', '네이버카페'))
with col3:
    input_str = st.text_input('제거할 키워드')
    stopwords = [x.strip() for x in input_str.split(',')]

