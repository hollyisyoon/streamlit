import streamlit as st
from annotated_text import annotated_text

# 데이터프레임 생성
import pandas as pd
df = pd.DataFrame({'키워드':['참', '걸'], '평균 영향도':[0.559585, 0.476684], 'URL':['https://band.us/band/86294308/post/322', 'https://band.us/band/86294308/post/358']})

# 키워드와 평균 영향도를 annoted_text로 변환하는 함수
def format_keyword_score(row):
    keyword = row['키워드']
    score = row['평균 영향도']
    text = f"{keyword} ({score:.3f})"
    return text

# 각 행을 annotated_text로 변환
texts = []
for i, row in df.iterrows():
    keyword_score_text = format_keyword_score(row)
    url = row['URL']
    texts.append((keyword_score_text, url))

# annotated_text 출력
annotated_text(*texts)
