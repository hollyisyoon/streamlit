


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
import streamlit as st

df2 = pd.read_csv('/app/streamlit/data/df_트렌드_github.csv')
df2['날짜'] = pd.to_datetime(df2['날짜'])

keyword1 = st.text_input('궁금한 키워드', value='제라늄')

import pandas as pd

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

result = get_TOP_10(df2, keyword1)

if result is not None:
    st.dataframe(result)
else:
    st.write("No results found.")





# df = pd.read_csv('/app/streamlit/data/df_트렌드_github.csv')
# df['날짜'] = pd.to_datetime(df['날짜'])

# def extract_df(df, media, start_date, end_date, effect_size):
#     start_date = pd.Timestamp(start_date)
#     end_date = pd.Timestamp(end_date)
#     standard_df = df[(df['매체'] == media) & (df['날짜'] >= start_date) & (df['날짜'] <= end_date) & (df['영향도'] >= effect_size)]
#     range_days = (end_date - start_date) + timedelta(days = 1)
#     new_day = start_date - range_days
#     new_day = pd.Timestamp(new_day)
#     new_df = df[(df['매체'] == media) & (df['날짜'] >= new_day) & (df['날짜'] < start_date) & (df['영향도'] >= effect_size)]   
#     return standard_df, new_df

# standard_df, new_df = extract_df(df, '식물갤러리', df['날짜'][3000], df['날짜'][0], 0)

# def convert_to_markdown(row):
#     return f"[`{row['키워드']} | {row['평균 영향도']:.6f}`]({row['URL']})"

# def make_keyword_tag(df):
#     markdown_rows = df.apply(convert_to_markdown, axis=1).tolist()
#     markdown_text = '   '.join(markdown_rows)
#     return mdlit(f"""{markdown_text}""")

# def new_keyword(standard_df, new_df):
#     # 각각의 데이터프레임에서 title+content 칼럼을 추출하여 리스트로 변환
#     content_list_1 = []
#     content_list_1.extend(list(itertools.chain.from_iterable([eval(i) for i in standard_df['제목+내용(nng)']])))
#     content_list_2 = []
#     content_list_2.extend(list(itertools.chain.from_iterable([eval(i) for i in new_df['제목+내용(nng)']])))

#     new_keywords = set(content_list_2) - set(content_list_1)   
#     result_dict = {}

#     # 이번달에만 있는 
#     for word in new_keywords:
#         word_df = new_df[new_df['제목+내용(nng)'].str.contains(word)]
#         if len(word_df) > 0:
#             avg_views = word_df['영향도'].mean()
#             urls = word_df['URL'].tolist()
#             result_dict[word] = {'평균 영향도': float(avg_views), 'URL': urls}
            
#     # 조회수 높은순으로 정렬        
#     result_dict = dict(sorted(result_dict.items(), key=lambda item: item[1]['평균 영향도'], reverse=True))    
    
#     # 결과 딕셔너리를 데이터프레임으로 변환
#     keywords = []
#     avg_views = []
#     urls = []
    
#     for key, value in result_dict.items():
#         keywords.append(key)
#         avg_views.append(value['평균 영향도'])
#         urls.append('\n'.join(value['URL']))
    
#     result_df = pd.DataFrame({
#         '키워드': keywords,
#         '평균 영향도': avg_views,
#         'URL': urls
#     })
    
#     return result_df

# new_keyword = new_keyword(standard_df, new_df)
# make_keyword_tag(new_keyword)

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


