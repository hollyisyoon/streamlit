import streamlit as st
import streamlit.components.v1 as components

# CSS 스타일 정의
css_code = """
<style>
    .custom-sidebar {
        padding: 20px;
        background-color: #f2f2f2;
        font-size: 18px;
        color: #333;
    }
</style>
"""

# 컴포넌트로 CSS 코드 추가
st.sidebar.markdown(f"<style>{css_code}</style>", unsafe_allow_html=True)

# 커스텀 클래스를 적용한 div 요소로 사이드바 컨텐츠 생성
st.sidebar.markdown("""
    <div class="custom-sidebar">
        <h2><a href="#section1">서브타이틀 1</a></h2>
        <h2><a href="#section2">서브타이틀 2</a></h2>
    </div>
""", unsafe_allow_html=True)

# 메인 콘텐츠 영역
st.write("여기에 메인 콘텐츠를 작성합니다.")

# 메인 콘텐츠 영역
st.markdown("<h2 id='section1'>서브타이틀 1 내용</h2>", unsafe_allow_html=True)
st.write("여기에 서브타이틀 1의 내용을 작성합니다.")

st.markdown("<h2 id='section2'>서브타이틀 2 내용</h2>", unsafe_allow_html=True)
st.write("여기에 서브타이틀 2의 내용을 작성합니다.")

st.markdown("<h2 id='section3'>서브타이틀 3 내용</h2>", unsafe_allow_html=True)
st.write("여기에 서브타이틀 3의 내용을 작성합니다.")