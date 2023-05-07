import streamlit as st
import streamlit.components.v1 as components

# JavaScript 함수 정의 (클릭 이벤트 처리)
js_code = """
<script>
    function scrollToContent(sectionId) {
        const element = document.getElementById(sectionId);
        element.scrollIntoView({ behavior: 'smooth' });
    }
</script>
"""

# 컴포넌트로 HTML 코드 추가
components.html(js_code)

# 사이드바에 HTML을 추가하여 서브타이틀 클릭 이벤트 처리
st.sidebar.markdown("""
    <h2 onclick="scrollToContent('section1')">서브타이틀 1</h2>
    <h2 onclick="scrollToContent('section2')">서브타이틀 2</h2>
    <h2 onclick="scrollToContent('section3')">서브타이틀 3</h2>
""", unsafe_allow_html=True)

# 메인 콘텐츠 영역
st.markdown("<h1 id='section1'>서브타이틀 1 내용</h1>", unsafe_allow_html=True)
st.write("여기에 서브타이틀 1의 내용을 작성합니다.")

st.markdown("<h1 id='section2'>서브타이틀 2 내용</h1>", unsafe_allow_html=True)
st.write("여기에 서브타이틀 2의 내용을 작성합니다.")

st.markdown("<h1 id='section3'>서브타이틀 3 내용</h1>", unsafe_allow_html=True)
st.write("여기에 서브타이틀 3의 내용을 작성합니다.")
