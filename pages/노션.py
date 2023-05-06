import streamlit as st

# Custom CSS styles
STYLE = """
.callout {
    padding: 1em;
    border-radius: 0.5em;
    background-color: #F8F8F8;
    border-left: 4px solid #f74040;
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

import pandas as pd

df = pd.DataFrame({
    '키워드': ['아이', '헬로', '바이', '안녕', '그냥', '오늘'],
    '상승률': ['44%', '50%', '50%', '22%', '22%', '10%'],
    'URL': ['https://www.naver.com', 'https://www.google.com', 'https://www.google.com',
            'https://www.daum.net', 'https://www.kakao.com', 'https://www.ul.com']
})

# Group by URL
groups = df.groupby('URL')

# Initialize key counter
key_counter = 1

# Generate HTML tags
html_tags = ''
for url, group in groups:
    keywords = ' '.join(group['키워드'])
    percent = group['상승률'].iloc[0]
    key_counter = (key_counter % 4) + 1  # Reset key counter after reaching 4
    html_tags += f"<a id='key{key_counter}' href='{url}'>{keywords}</a><b>({percent}🔥)</b>&nbsp;"

# Display the generated HTML tags
st.markdown(f"<style>{STYLE}</style>", unsafe_allow_html=True)
st.markdown(f"""
    <div class='callout'>
    <h1>급상승 키워드📈</h1>
    {html_tags}
    </div>""",
    unsafe_allow_html=True
)

# st.markdown(f"<style>{STYLE}</style>", unsafe_allow_html=True)
# st.markdown(
#     """
#     <div class="callout">
#         <a id="key1" href="https://www.naver.com">키워드1 키워드2</a>
#         <b>(44%🔥)</b>&nbsp;
#         <a id="key2" href="https://www.naver.com">키워드2</a>&nbsp;
#         <a id="key3" href="https://www.naver.com">키워드3</a>&nbsp;

#     </div>
#     """,
#     unsafe_allow_html=True
# )


st.markdown(
    """
    <div class="callout">
        <li> <b>안녕하세요 이것은 제목이고요</b> | 키워드1 키워드2 키워드3 키워드4 <a href="https://www.naver.com"> 링크 </a> </li>
        <li> <b>안녕하세요 이것은 제목이고요</b> | 키워드1 키워드2 키워드3 키워드4 키워드4 키워드4 키워드4 <a href="https://www.naver.com"> 링크 </a> </li>
    </div>
    """,
    unsafe_allow_html=True
)

st.code(
    """
    <div class="callout">
        &lt;a href="https://www.naver.com"&gt;키워드&lt;/a&gt; 키워드 키워드 안녕하세요 오오오잉ㅇ
    </div>
    """,
    language="html"
)

# Apply custom CSS styles
st.markdown(f"<style>{STYLE}</style>", unsafe_allow_html=True)

# Create a callout using Markdown
st.markdown(
    """
    <div class="callout">
        <code>&lt;a href="https://www.naver.com"&gt;키워드&lt;/a&gt; 키워드 키워드 안녕하세요 오오오잉ㅇ</code>
    </div>
    """,
    unsafe_allow_html=True
)