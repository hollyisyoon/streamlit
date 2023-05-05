
링크를 클릭 가능한 형태로 변경해주기 위해서 annotated_text() 함수의 mark_text() 메소드를 사용하여 텍스트에 앵커 태그(anchor tag)를 추가하면 됩니다. 이때 앵커 태그의 href 속성을 링크 URL로 지정해주면 됩니다.

그리고 호버 이벤트를 처리하기 위해서는 annotated_text() 함수의 add_style() 메소드를 사용하여 CSS 스타일을 추가해주어야 합니다. 이때 CSS 스타일의 cursor 속성을 pointer로 설정하면 마우스 커서가 포인터 모양으로 변경되어 클릭 가능한 링크임을 사용자에게 알릴 수 있습니다.

아래는 수정된 코드 예시입니다.

python
Copy code
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
    link = row['URL']
    texts.append((keyword_score_text, score, link))

st.write(texts)