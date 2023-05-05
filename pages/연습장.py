


import streamlit as st
from htbuilder import div, a, span  # htbuilder 패키지에서 필요한 함수 가져오기
from htbuilder.units import px
from annotated_text import annotated_text, parameters
from markdownlit import mdlit


# PADDING=(rem(0.25), rem(0.5))
# BORDER_RADIUS=rem(1)
# # LABEL_FONT_SIZE=rem(0.75)
# LABEL_OPACITY=0.5
# LABEL_SPACING=rem(1)

# 데이터프레임 생성
import pandas as pd
import itertools

df_concat_github = pd.read_csv('https://raw.githubusercontent.com/hollyisyoon/streamlit/main/data/df_%E1%84%90%E1%85%B3%E1%84%85%E1%85%A6%E1%86%AB%E1%84%83%E1%85%B3_github.csv')

df_concat_github['날짜'] = pd.to_datetime(df_concat_github['날짜'])

def extract_df(df, media, start_date, end_date, effect_size):
    start_date = pd.Timestamp(start_date)
    end_date = pd.Timestamp(end_date)
    standard_df = df[(df['매체'] == media) & (df['날짜'] >= start_date) & (df['날짜'] <= end_date) & (df['영향도'] >= effect_size)]
    range_days = (end_date - start_date) + timedelta(days = 1)
    new_day = start_date - range_days
    new_day = pd.Timestamp(new_day)
    new_df = df[(df['매체'] == media) & (df['날짜'] >= new_day) & (df['날짜'] < start_date) & (df['영향도'] >= effect_size)]
    
    return standard_df, new_df

standard_df, new_df = extract_df(df_concat_github, '식물갤러리', df_concat_github['날짜'][3000], df_concat_github['날짜'][0], 0)

def convert_to_markdown(row):
    return f"[`{row['키워드']} | {row['평균 영향도']:.6f}`]({row['URL']})"

def make_keyword_tag(df):
    markdown_rows = df.apply(convert_to_markdown, axis=1).tolist()
    markdown_text = '   '.join(markdown_rows)
    return mdlit(f"""{markdown_text}""")

def new_keyword(standard_df, new_df):
    # 각각의 데이터프레임에서 title+content 칼럼을 추출하여 리스트로 변환
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
    return result_dict

new_keyword = pd.DataFrame(new_keyword(standard_df, new_df), columns=['키워드', '평균 영향도', 'URL'])
make_keyword_tag(new_keyword)




# 색깔 포함 #####
    # def format_keyword_score(row):
    #     keyword = row['키워드']
    #     return keyword

    # # 각 행을 annotated_text로 변환
    # texts = []
    # for i, row in df.iterrows():
    #     keyword_score_text = format_keyword_score(row)
    #     score = row['평균 영향도'] * 100
    #     score = f'{score:.0f}'
    #     texts.append((keyword_score_text, score))

    # # annotated_text 출력
    # annotated_text(*texts)



### 글씨만 나옴#####
# 키워드와 평균 영향도를 annoted_text로 변환하는 함수
# def format_keyword_score(row):
#     keyword = row['키워드']
#     return keyword

# # 각 행을 annotated_text로 변환
# texts = []
# for i, row in df.iterrows():
#     keyword_score_text = format_keyword_score(row)
#     score = row['평균 영향도']
#     score = f'{score:.3f}'
#     link = row['URL']
#     texts.append((keyword_score_text, score, link))

# annotated_text(*texts)


