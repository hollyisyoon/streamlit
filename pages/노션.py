import streamlit as st

# Custom CSS styles
STYLE = """
.callout {
    padding: 1em;
    border-radius: 0.5em;
    background-color: #F8F8F8;
    border-left: 4px solid #FF9800;
    margin-bottom: 1em;
    color: black;
}
"""

# Apply custom CSS styles
st.markdown(f"<style>{STYLE}</style>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="callout">
        <a href="https://www.naver.com">키워드</a> 키워드 키워드 안녕하세요 오오오잉ㅇ
    </div>
    """,
    unsafe_allow_html=True
)

