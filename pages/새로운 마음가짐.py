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
import itertools

rain(emoji="🦝",
    font_size=54,
    falling_speed=10,
    animation_length="infinite")

######데이터#########
def to_list(text):
    return ast.literal_eval(text)

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

with col2:
    media = st.selectbox('매체',('식물갤러리', '식물병원', '네이버카페', '네이버블로그', '네이버포스트'))

with col3:
    temp_effect_size = st.slider('영향도 볼륨', 0, 100, 30)
    effect_size = (100-int(temp_effect_size))/100

standard_df, new_df = extract_df(df, media, start_date, end_date, effect_size)

#####워드 클라우드########
##Count기준###
def get_tfidf_top_words(df, keyword_no):
    tfidf_vectorizer = TfidfVectorizer(stop_words=stopwords)
    tfidf = tfidf_vectorizer.fit_transform(df['제목+내용(nng)'].values)
    tfidf_df = pd.DataFrame(tfidf.todense(), columns=tfidf_vectorizer.get_feature_names_out())
    tfidf_top_words = tfidf_df.sum().sort_values(ascending=False).head(keyword_no).to_dict()
    tfidf_top_words = dict(tfidf_top_words)
    return tfidf_top_words

def get_count_top_words(df, keyword_no):
    count_vectorizer = CountVectorizer(stop_words=stopwords)
    count = count_vectorizer.fit_transform(df['제목+내용(nng)'].values)
    count_df = pd.DataFrame(count.todense(), columns=count_vectorizer.get_feature_names_out())
    count_top_words = count_df.sum().sort_values(ascending=False).head(keyword_no).to_dict()
    return count_top_words

###시각화####
col1, col2 = st.beta_columns((0.2, 0.8))
with col1:
    type = st.selectbox('기준',('단순 빈도(Countvecterize)','상대 빈도(TF-IDF)'))
    keyword_no = st.number_input("키워드 볼륨", value=100, min_value=1, step=1)
    input_str = st.text_input('제거할 키워드')
    stopwords = [x.strip() for x in input_str.split(',')]

with col2:
    try :
        if type == '단순 빈도(Countvecterize)' :
            words = get_count_top_words(standard_df, keyword_no)
        else :
            words = get_tfidf_top_words(standard_df, keyword_no)

        #워드클라우드
        wc = WordCloud(background_color="white", colormap='Spectral', contour_color='steelblue', font_path="/app/streamlit/font/Pretendard-Bold.otf")
        wc.generate_from_frequencies(words)

        ###########동적 워드 클라우드####################
        # 컬러 팔레트 생성
        word_list=[]
        freq_list=[]
        fontsize_list=[]
        position_list=[]
        orientation_list=[]
        color_list=[]

        for (word, freq), fontsize, position, orientation, color in wc.layout_:
            word_list.append(word)
            freq_list.append(freq)
            fontsize_list.append(fontsize)
            position_list.append(position)
            orientation_list.append(orientation)
            color_list.append(color)

        # get the positions
        x=[]
        y=[]
        for i in position_list:
            x.append(i[0])
            y.append(i[1])

        # WordCloud 시각화를 위한 Scatter Plot 생성
        fig = go.Figure(go.Scatter(
            x=x, y=y, mode="text",
            text=word_list,
            textfont=dict(size=fontsize_list, color=color_list),
        ))
        fig.update_layout(xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False), hovermode='closest')
        st.plotly_chart(fig, use_container_width=True)

    except :
        st.warning('영향도 범위를 조정해주세요! 데이터가 부족합니다 👻')    


#### 키워드 큐레이팅 #####
### 신규 키워드 ###
def convert_to_markdown(row):
    return f"[`{row['키워드']} | {row['평균 영향도']:.6f}`]({row['URL']})"

def make_keyword_tag(df):
    markdown_rows = df.apply(convert_to_markdown, axis=1).tolist()
    markdown_text = '   '.join(markdown_rows)
    return mdlit(f"""{markdown_text}""")

def new_keyword(standard_df, new_df):
    df['제목+내용(nng)'] = df['제목+내용(nng)'].map(to_list)
    content_list_1 = []
    content_list_1.extend(list(itertools.chain.from_iterable([eval(i) for i in standard_df['제목+내용(nng)']])))
    content_list_2 = []
    content_list_2.extend(list(itertools.chain.from_iterable([eval(i) for i in new_df['제목+내용(nng)']])))

    new_keywords = set(content_list_2) - set(content_list_1)   
    result_dict = {}
    # 이번달에만 있는 
    for word in new_keywords:
        word_df = new_df[new_df['제목+내용(nng)'].str.contains(word)]
        if len(word_df) > 0:
            avg_views = word_df['영향도'].mean()
            urls = word_df['URL'].tolist()
            result_dict[word] = {'평균 영향도': float(avg_views), 'URL': urls}
            
    # 조회수 높은순으로 정렬        
    result_dict = dict(sorted(result_dict.items(), key=lambda item: item[1]['평균 영향도'], reverse=True))    

    # 결과 딕셔너리를 데이터프레임으로 변환
    keywords = []
    avg_views = []
    urls = []
    
    for key, value in result_dict.items():
        keywords.append(key)
        avg_views.append(value['평균 영향도'])
        urls.append('\n'.join(value['URL']))
    
    result_df = pd.DataFrame({
        '키워드': keywords,
        '평균 영향도': avg_views,
        'URL': urls
    })
    
    return result_df

new_keyword = new_keyword(standard_df, new_df)
make_keyword_tag(new_keyword)
new_keyword
standard_df, new_df
