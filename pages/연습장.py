import streamlit as st
from annotated_text import annotated_text

# 데이터프레임 생성
import pandas as pd
df = pd.DataFrame({'키워드':['참', '걸'], '평균 영향도':[0.559585, 0.476684], 'URL':['https://band.us/band/86294308/post/322', 'https://band.us/band/86294308/post/358']})

# 키워드와 평균 영향도를 annoted_text로 변환하는 함수
def format_keyword_score(row):
    keyword = row['키워드']
    return keyword

# 각 행을 annotated_text로 변환
texts = []
for i, row in df.iterrows():
    keyword_score_text = format_keyword_score(row)
    score = row['평균 영향도']
    score = f'{score:.3f}'
    url = row['URL']
    tag = f"<a href='{url}' title='{url}' target='_blank'>{keyword_score_text} ({score})</a>"
    texts.append(tag)

# annotated_text를 HTML 형식으로 변환하여 출력
st.write(annotated_text(*texts).to_html(escape=False), unsafe_allow_html=True)
