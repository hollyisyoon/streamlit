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

.callout a #key1 {
    color: #5c5c5c;
    text-decoration: underline;
    text-decoration-color: gray;
    background-color: #ff7d7d;
}

.callout a #key2 {
    color: #5c5c5c;
    text-decoration: underline;
    text-decoration-color: gray;
    background-color: #ff9696;
}

.callout a #key3 {
    color: #5c5c5c;
    text-decoration: underline;
    text-decoration-color: gray;
    background-color: #ffbaba;
}
"""

# Apply custom CSS styles
st.markdown(f"<style>{STYLE}</style>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="callout">
        <a id="key1" href="https://www.naver.com">키워드1</a>
        <a id="key2" href="https://www.naver.com">키워드2</a>
        <a id="key3" href="https://www.naver.com">키워드3</a>
    </div>
    """
)


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