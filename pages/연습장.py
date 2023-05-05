import streamlit as st
from annotated_text import annotated_text

# 데이터프레임 생성
import pandas as pd
df = pd.DataFrame({'키워드':['참', '걸'], '평균 영향도':[0.559585, 0.476684], 'URL':['https://band.us/band/86294308/post/322', 'https://band.us/band/86294308/post/358']})

# 클릭 시 URL을 열도록 하는 JavaScript 코드
click_callback = """
<script>
    const links = document.querySelectorAll('.custom-link')
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault()
            window.open(link.href, '_blank')
        })
    })
</script>
"""

# 키워드와 평균 영향도를 annotated_text로 변환하는 함수
def format_keyword_score(row):
    keyword = row['키워드']
    url = row['URL']
    return f'<a class="custom-link" href="{url}">{keyword}</a>'

# 각 행을 annotated_text로 변환
texts = []
for i, row in df.iterrows():
    keyword_score_text = format_keyword_score(row)
    score = row['평균 영향도']
    score = f'{score:.3f}'
    texts.append((keyword_score_text, score))

# annotated_text 출력
annotated_text(*texts)

# JavaScript 코드 실행
st.components.v1.html(click_callback)
