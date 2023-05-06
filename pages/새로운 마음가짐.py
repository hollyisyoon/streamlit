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

rain(emoji="🦝",
    font_size=54,
    falling_speed=5,
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
    return f"[`{row['키워드']} | {row['평균 영향도']*100:.0f}`]({row['URL']})"

def convert_to_markdown2(row):
    return f"[`{row['키워드']} | {row['상승률']*100:.0f}`]({row['URL']})"

def make_keyword_tag(df):
    markdown_rows = df.apply(convert_to_markdown, axis=1).tolist()
    markdown_text = '   '.join(markdown_rows)
    return mdlit(f"""{markdown_text}""")

def make_keyword_tag2(df):
    markdown_rows = df.apply(convert_to_markdown2, axis=1).tolist()
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

    return result_df[:20]

def rising_keyword(standard_df, new_df):
    # 데이터 합치기 
    df = pd.concat([standard_df, new_df])
    df['제목+내용(nng)'] = df['제목+내용(nng)'].map(to_list)
    
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

    for word, data in sorted(result.items(), key=lambda x: x[1]['상승률'], reverse=True):
        if data['상승률']>0:
            keywords.append(word)
            ups.append(f"{data['상승률']}%")
            urls.append(data['URL'])

    result_df = pd.DataFrame({
        '키워드': keywords,
        '상승률': ups,
        'URL': urls
    })

    if len(result_df.index) >= 1 :
        return result_df
    
### 키워드 ###
st.subheader('✨ 신규 키워드')
try:
    new_keyword = new_keyword(standard_df, new_df)
    make_keyword_tag(new_keyword)
except:
    st.warning("⚠️ 해당 기간 동안 신규 키워드가 존재하지 않습니다")

st.subheader('🔥 급상승 키워드')
try:
    rising_keyword = rising_keyword(standard_df, new_df)
    make_keyword_tag2(rising_keyword)
except:
    st.warning("⚠️ 해당 기간 동안 급상승 키워드가 존재하지 않습니다")

########### 키워드 DeepDive ###########
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

def get_df(df, word1, *args):
    # word1 은 반드시 입력해야 하는 기준
    # 입력한 단어 중 하나 이상이 포함된 행 찾기
    df['날짜'] = pd.to_datetime(df['날짜'])
    result = df[(df['매체'] == '식물갤러리') | (df['매체'] == '식물병원')]
    result = result[(result['날짜'] >= '2022-04-27') & (result['날짜'] <= '2023-04-26')]
    keywords = [word1] + list(args)

    return keywords
    # result = result[result['제목+내용(nng)'].str.contains('|'.join(keywords))]
    
    # # 입력한 단어 중 하나라도 포함되어 있지 않은 경우 오류 메시지를 반환
    # for arg in keywords:
    #     if arg not in ' '.join(result['제목+내용(nng)'].tolist()):
    #         return f"'{arg}'는 한 번도 언급되지 않은 키워드입니다. 다시 입력해주세요."
    
    # return result, keywords

def plot_keyword_impact_grey(df, keywords):
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
        
    fig.update_layout(title_text="시간별 키워드 영향도", xaxis_title="날짜", yaxis_title="평균 영향도")
    st.plotly_chart(fig, use_container_width=True)

keyword2
get_df(df, keyword1, keyword2)
# plot_keyword_impact_grey(deepdive_df, keyword_list)
