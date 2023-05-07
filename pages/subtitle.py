import streamlit as st
import streamlit.components.v1 as components

# CSS 스타일 정의
css_code = """
<style>
    a.custom-link {
        display: block;
        font-size: 24px;
        font-weight: bold;
        color: #333;
        text-decoration: none;
    }
</style>
"""

# 컴포넌트로 CSS 코드 추가
components.html(css_code)

# 사이드바에 HTML을 추가하여 서브타이틀 클릭 이벤트 처리
st.sidebar.markdown("""
    <a class="custom-link" href="#section1">서브타이틀 1</a>
    <a class="custom-link" href="#section2">서브타이틀 2</a>
    <a class="custom-link" href="#section3">서브타이틀 3</a>
""", unsafe_allow_html=True)

# 메인 콘텐츠 영역
st.markdown("<h2 id='section1'>서브타이틀 1 내용</h2>", unsafe_allow_html=True)
st.write("여기에 서브타이틀 1의 내용을 작성합니다.")

st.markdown("<h2 id='section2'>서브타이틀 2 내용</h2>", unsafe_allow_html=True)
st.write("여기에 서브타이틀 2의 내용을 작성합니다.")

st.markdown("<h2 id='section3'>서브타이틀 3 내용</h2>", unsafe_allow_html=True)
st.write("여기에 서브타이틀 3의 내용을 작성합니다.")
