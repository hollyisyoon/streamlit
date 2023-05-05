


import streamlit as st
from htbuilder import div, a, span  # htbuilder 패키지에서 필요한 함수 가져오기
from htbuilder.units import px
from annotated_text import annotated_text, parameters

rem = unit.rem

# PADDING=(rem(0.25), rem(0.5))
# BORDER_RADIUS=rem(1)
# # LABEL_FONT_SIZE=rem(0.75)
# LABEL_OPACITY=0.5
# LABEL_SPACING=rem(1)

# 데이터프레임 생성
import pandas as pd
df = pd.DataFrame({'키워드':['참', '걸'], '평균 영향도':[0.559585, 0.476684], 'URL':['https://band.us/band/86294308/post/322', 'https://band.us/band/86294308/post/358']})


#link 시도###
# 색깔 포함, 클릭 가능한 링크 추가
def format_keyword_score(row):
    keyword = row["키워드"]
    return keyword

# 각 행을 annotated_text로 변환
texts = []
for i, row in df.iterrows():
    keyword_score_text = format_keyword_score(row)
    score = row["평균 영향도"] * 100
    score = f"{score:.0f}"
    url = row["URL"]
    # 클릭 가능한 링크 추가
    keyword_span = span(
        keyword_score_text,
        style=f"background-color: {'#F9CACA' if score == '100' else '#FDF0D2'}; padding: 0.15rem 0.25rem; border-radius: 0.25rem",
    )
    url_span = span(
        a("↗", href=url, target="_blank"),
        style="color: #666; font-size: 0.75rem; padding-left: 0.25rem",
    )
    texts.append((keyword_span, url_span))

# annotated_text 출력
st.markdown(
    div(style=f"padding: {px(8)};")(texts), unsafe_allow_html=True
)


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


