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

######데이터#########
df = pd.read_csv('/app/streamlit/data/df_트렌드_github.csv', encoding='utf-8')

def extract_df(df, media, start_date, end_date, effect_size):
    start_date = pd.Timestamp(start_date)
    end_date = pd.Timestamp(end_date)
    df['날짜'] = df['날짜'].apply(lambda x: pd.to_datetime(x))
    standard_df = df[(df['매체'] == media) & (df['날짜'] >= start_date) & (df['날짜'] <= end_date) & (df['영향도'] >= effect_size)]

    range_days = (end_date - start_date) + timedelta(days = 1)
    new_day = start_date - range_days
    new_day = pd.Timestamp(new_day)
    new_df = df[(df['매체'] == media) & (df['날짜'] >= new_day) & (df['날짜'] <= start) & (df['영향도'] >= effect_size)]
    
    return standard_df, new_df

######################대시보드
st.title('외부 트렌드 모니터링 대시보드')

#### 인풋 필터 #####
col1, col2, col3 = st.beta_columns(3)

min_date = datetime(2022, 7, 25)
max_date = datetime(2023, 4, 26)
with col1:
    start_date = st.date_input("시작 날짜",
                               value=datetime(2023,4,1),
                               min_value=min_date,
                               max_value=max_date - timedelta(days=7))
    # 끝 날짜를 선택할 때 최소 날짜는 시작 날짜이며, 최대 날짜는 90일 이전까지로 제한
    end_date = st.date_input("끝 날짜",
                             value=datetime(2023,4,15),
                             min_value=start_date + timedelta(days=7),
                             max_value=start_date + timedelta(days=90))
start_date = pd.Timestamp(start_date)
end_date = pd.Timestamp(end_date)

with col2:
    media = st.selectbox('매체',('식물갤러리', '식물밴드', '네이버카페', '네이버블로그', '네이버포스트'))

with col3:
    temp_effect_size = st.slider('영향도 볼륨', 0, 100, 30)
    effect_size = (100-int(temp_effect_size))/100

standard_df, new_df = extract_df(df, media, start_date, end_date, effect_size)

#####워드 클라우드########
col1, col2 = st.beta_columns((0.2, 0.8))
with col1:
    type = st.selectbox('기준',('상대 빈도(TF-IDF)','단순 빈도(Countveterize)'))
    keyword_no = st.number_input("키워드 볼륨", value=100, min_value=1, step=1)
    input_str = st.text_input('제거할 키워드', value='식물')
    stopwords = [x.strip() for x in input_str.split(',')]
with col2:
    pd.DataFrame(standard_df)
    # #워드클라우드
    # wc = WordCloud(background_color="white", colormap='Spectral', contour_color='steelblue', font_path="/app/busypeople-stramlit/font/NanumBarunGothic.ttf")
    # wc.generate_from_frequencies(words)

    # ###########동적 워드 클라우드####################
    # # 컬러 팔레트 생성
    # word_list=[]
    # freq_list=[]
    # fontsize_list=[]
    # position_list=[]
    # orientation_list=[]
    # color_list=[]

    # for (word, freq), fontsize, position, orientation, color in wc.layout_:
    #     word_list.append(word)
    #     freq_list.append(freq)
    #     fontsize_list.append(fontsize)
    #     position_list.append(position)
    #     orientation_list.append(orientation)
    #     color_list.append(color)

    # # get the positions
    # x=[]
    # y=[]
    # for i in position_list:
    #     x.append(i[0])
    #     y.append(i[1])

    # # WordCloud 시각화를 위한 Scatter Plot 생성
    # fig = go.Figure(go.Scatter(
    #     x=x, y=y, mode="text",
    #     text=word_list,
    #     textfont=dict(size=fontsize_list, color=color_list),
    # ))
    # fig.update_layout(title="WordCloud", xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    #                 yaxis=dict(showgrid=False, zeroline=False, showticklabels=False), hovermode='closest')
    # st.plotly_chart(fig, use_container_width=True)