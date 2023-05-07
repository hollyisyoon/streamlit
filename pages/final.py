import koreanize_matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.colors import to_rgba
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
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

#스트림잇
import streamlit as st
from streamlit_extras.let_it_rain import rain
from streamlit_tags import st_tags
import warnings
warnings.filterwarnings("ignore", message="PyplotGlobalUseWarning")

#계산
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

############## 사이드바
# st.sidebar.markdown(f"<style>{css_code}</style>", unsafe_allow_html=True)
# st.sidebar.markdown("""
#     <div class="custom-sidebar">
#         <h2><a href="#section1">🪄 키워트 발굴</a></h2>
#         <h2><a href="#section2">💎 키워드 큐레이션</a></h2>
#         <h2><a href="#section3">⏳ 시기별 키워드 영향도</a></h2>
#         <h2><a href="#section4">서브타이틀 4</a></h2>
#     </div>
# """, unsafe_allow_html=True)

##############메인 콘텐츠
st.title("외부 트렌드 모니터링 대시보드")

#########Section1 - wordcloud############
st.markdown("<h2 id='section1'>🪄 키워트 발굴</h2>", unsafe_allow_html=True)

##데이터##
def to_list(text):
    return ast.literal_eval(text)

df = pd.read_csv('/app/streamlit/data/df_트렌드_github.csv')
df['날짜'] = pd.to_datetime(df['날짜'])
def extract_df(df, media, start_date, end_date, effect_size):
    start_date = pd.Timestamp(start_date)
    end_date = pd.Timestamp(end_date)
    standard_df = df[(df['매체'] == media) & (df['날짜'] >= start_date) & (df['날짜'] <= end_date) & (df['영향도'] >= effect_size)]
    range_days = (end_date - start_date) + timedelta(days = 1)
    new_day = start_date - range_days
    new_day = pd.Timestamp(new_day)
    new_df = df[(df['매체'] == media) & (df['날짜'] >= new_day) & (df['날짜'] < start_date) & (df['영향도'] >= effect_size)]    
    return standard_df, new_df

##인풋 필터 - 전체용##
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
    media = st.selectbox('매체',('식물갤러리', '식물병원', '네이버카페', '네이버블로그', '네이버포스트'), help="확인하고 싶은 외부 데이터의 매체를 선택할 수 있습니다.")
with col3:
    temp_effect_size = st.slider('영향도 볼륨', 0, 100, 83, help="각 매체별 콘텐츠의 반응도를 점수화한 값입니다. 0에 가까울 수록 영향도가 높습니다.")
    effect_size = (100-int(temp_effect_size))/100
standard_df, new_df = extract_df(df, media, start_date, end_date, effect_size)

##인풋 필터 - 워드클라우드용##
expander = st.expander('워드 클라우드 세부필터')
with expander:
    col1, col2= st.beta_columns(2)    
    with col1:
        type = st.selectbox('기준',('단순 빈도(Countvectorizer)','상대 빈도(TF-IDF)'), 
                            help="""단순빈도란 문서 내 각 단어가 나타난 빈도 즉, 나타난 횟수를 세서 만든 값입니다. 
                            상대빈도는 단어가 문서 내에서 얼마나 중요한지를 나타내는 지표입니다.""")
    with col2:
        keyword_no = st.number_input("키워드 볼륨", value=100, min_value=1, step=1,
                                     help="워드 클라우드를 통해 보고 싶은 단어의 갯수를 제어할 수 있습니다.")   
    stopwords = st_tags(
        label = '제거할 키워드',
        text = '직접 입력해보세요',
        value = ['식물', '화분'],
        suggestions = ['식물', '화분'],
        key = '1')

##워드 클라우드##
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

try :
    if type == '단순 빈도(Countvecterize)' :
        words = get_count_top_words(standard_df, keyword_no)
    else :
        words = get_tfidf_top_words(standard_df, keyword_no)

    #워드클라우드
    wc = WordCloud(background_color="white", colormap='Spectral', contour_color='steelblue', font_path="/app/streamlit/font/Pretendard-Bold.otf")
    wc.generate_from_frequencies(words)

    ## 동적 워드 클라우드 ##
    # 컬러 팔레트 생성
    word_list = []
    freq_list = []
    fontsize_list = []
    position_list = []
    orientation_list = []
    color_list = []

    for (word, freq), fontsize, position, orientation, color in wc.layout_:
        word_list.append(word)
        freq_list.append(freq)
        fontsize_list.append(fontsize)
        position_list.append(position)
        orientation_list.append(orientation)
        color_list.append(color)

    # get the positions
    x = []
    y = []
    for i in position_list:
        x.append(i[0])
        y.append(i[1])

    # WordCloud 시각화를 위한 Scatter Plot 생성
    hover_text = word_list  # 키워드만 포함한 텍스트 생성

    # 숫자값을 원하는 형식으로 표시하기 위한 hovertemplate 설정
    hover_template = "<b>%{text}</b><br>Count: %{customdata[0]}"

    fig = go.Figure(go.Scatter(
        x=x, y=y, mode="text",
        text=hover_text,
        customdata=list(zip(freq_list)),  # 숫자값을 customdata로 전달
        hovertemplate=hover_template,  # hovertemplate 설정
        textfont=dict(size=fontsize_list, color=color_list),
    ))

    fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        hovermode='closest'
    )

    st.plotly_chart(fig, use_container_width=True)

except :
    st.warning('영향도 범위를 조정해주세요! 데이터가 부족합니다')    

#########Section2 - 키워드 큐레이팅############
st.markdown("---")
st.markdown("<h2 id='section2'>💎 키워드 큐레이션</h2>", unsafe_allow_html=True)
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
            result_dict[word] = {'평균 영향도': round(float(avg_views), 2), 'URL': urls}
            
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

##키워드##
try:
    new_keyword = new_keyword(standard_df, new_df)
except:
    st.warning("⚠️ 해당 기간 동안 신규 키워드가 존재하지 않습니다")

try:
    rising_keyword = rising_keyword(standard_df, new_df)
except:
    st.warning("⚠️ 해당 기간 동안 급상승 키워드가 존재하지 않습니다")

##신규 키워드##
grouped_new_keyword = new_keyword.groupby('URL')
key_counter = 1
new_html_tags = ''
for url, group in grouped_new_keyword:
    keywords = ' | '.join(group['키워드'])
    percent = group['평균 영향도'].iloc[0]
    key_counter = (key_counter % 4) + 1  # Reset key counter after reaching 4
    new_html_tags += f"<a id='key{key_counter}' href='{url}'>{keywords}</a><b>({percent}💫)</b>&nbsp;"

##급상승 키워드##    
grouped_rising_keyword = rising_keyword.groupby('URL')
key_counter = 1
rising_html_tags = ''
for url, group in grouped_rising_keyword:
    keywords = ' | '.join(group['키워드'])
    percent = group['상승률'].iloc[0]
    key_counter = (key_counter % 4) + 1  # Reset key counter after reaching 4
    rising_html_tags += f"<a id='key{key_counter}' href='{url}'>{keywords}</a><b>({percent}🔥)</b>&nbsp;"

#HTML
st.markdown(f"<style>{STYLE}</style>", unsafe_allow_html=True)
st.markdown(f"""
    <h3>신규 키워드⭐️</h3>
    <div class='callout'>
    {new_html_tags}
    </div>""",
    unsafe_allow_html=True
)
st.markdown(f"""
    <h3>급상승 키워드📈</h3>
    <div class='callout'>
    {rising_html_tags}
    </div>""",
    unsafe_allow_html=True
)

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

#연관분석
if st.button('분석을 시작하기'):
    with st.spinner('분석 중입니다...'):
        all_keywords = [keyword1] + keyword2
        network_list = [eval(i) for i in df2['제목+내용(nng)']]
        네트워크 = 네트워크(network_list, all_keywords)
        if 네트워크 is not None:
            try:
                net = 네트워크[0]
                net.save_graph('/app/streamlit/pyvis_graph.html')
                HtmlFile = open('/app/streamlit/pyvis_graph.html', 'r', encoding='utf-8')
                components.html(HtmlFile.read(), height=600)
            except:
                st.warning('존재하지 않는 키워드예요.')
        else:
            st.warning('존재하지 않는 키워드예요.')
