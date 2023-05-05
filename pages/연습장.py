


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
# import pandas as pd
# df = pd.DataFrame({'키워드':['참', '걸'], '평균 영향도':[0.559585, 0.476684], 'URL':['https://band.us/band/86294308/post/322', 'https://band.us/band/86294308/post/358']})

#link 시도###
# URL 링크 생성 함수
mdlit(
Tired from [default links](https://extras.streamlit.app)?
Me too! Discover Markdownlit's `@()` operator. Just insert a link and it
will figure a nice icon and label for you!
Example: @(https://extras.streamlit.app)... better, right? You can
also @(🍐)(manually set the label if you want)(https://extras.streamlit.app)
btw, and play with a [red]beautiful[/red] [blue]set[/blue] [orange]of[/orange]
[violet]colors[/violet]. Another perk is those beautiful arrows -> <-
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


