import streamlit as st

STYLE = """
#key {
    color: #000;
    background-color: #FAF3DD;
    text-decoration: none;
}

.title {
    font-size: 24px;
    margin-top: 10px;
    font-weight: medium;
}

.callout {
    padding: 1em;
    border-radius: 0.5em;
    background-color: #F8F8F8;
    border-left: 4px solid #3B81F5;
    margin-bottom: 1em;
    color: black;
}

.team-member {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
    border-radius: 10px;
    padding: 10px 35px;
    background-color: #fafafa;
    -webkit-backdrop-filter: blur(5px);
}

.member-info {
  text-align: left;
  margin-left: 10px;
  padding: 20px;
}

.team-member .profile-image {
    width: 150px;
    height: 150px;
    border-radius: 50%;
}

.introduction {
  margin-top: 10px;
  font-size: 16px;
}

.cta-container-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    background-image: linear-gradient(rgba(0, 0, 0, 0.2), rgba(0, 0, 0, 0.2)));
    background-size: cover;
    padding: 10px;
    height: flex;
    border-radius: 10px;
}

.cta-container-wrapper.cta-container1 {
    background-image: url('https://i.pinimg.com/564x/7d/ef/e5/7defe5156cc72de1264011624e73e44c.jpg');
}

.cta-container-wrapper.cta-container2 {
    background-image: url('https://i.pinimg.com/564x/1f/87/d9/1f87d9f026f352bf2b662db576503186.jpg');
}

</style>
"""

st.markdown(f"<style>{STYLE}</style>", unsafe_allow_html=True)
st.markdown("""
  <div style="border-radius: 10px; overflow: hidden;">
  <img src="https://github.com/hollyisyoon/streamlit/blob/main/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202023-05-08%20%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE%2011.11.14.png?raw=true" 
  alt="메인 이미지"></img>
</div>""", unsafe_allow_html=True)
st.markdown(f"""
    <h2>바쁜 사람들 가이드</h2>
    <div class='callout'> 
    <li>바쁜 사람들은 1인 셀러들이 사업의 규모와 관계없이 <b>데이터에 기반한 의사결정</b>을 내릴 수 있는 환경을 제공하기 위해 제작되었습니다.</li> 
    <li>비즈니스 성장을 위해서는 운영하고 있는 채널에 대한 전반적인 데이터와 외부 데이터를 통해 문제점을 파악하고 알맞은 액션 플랜을 설계하는 것이 중요합니다.</li> 
    <li>바쁜 사람들은 유통 채널별 리뷰 데이터는 물론 경쟁사 리뷰 데이터에 대한 분석, 외부 데이터를 통한 트렌드 및 키워드 분석 결과를 분석가 없이도 손쉽게 분석할 수 있습니다.</li>
    </div>""",
    unsafe_allow_html=True
)

####CTA버튼####
cta_container1, cta_container2 = st.beta_columns(2)

# CTA container 1
with cta_container1:
    st.markdown(
        """
        <div class="cta-container-wrapper cta-container1">
            <div style='padding: 10px; border-radius: 10px'>
                <h2 style='color: white; text-align: center'>User Guide</h2>
                <p style='color: white; text-align: center'>바쁜 사람들이 처음이라면?</p>
                <p style='text-align: center'>
                    <a href='https://notion.so' target='_blank'>
                        <button style='background-color: white; color: #3B81F5; padding: 8px 16px; border-radius: 5px; border: none; font-weight: bold; cursor: pointer'>
                            살펴보기
                        </button>
                    </a>
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
with cta_container2:
    st.markdown(
        """
        <div class="cta-container-wrapper cta-container2">
            <div style='padding: 10px; border-radius: 10px'>
                <h2 style='color: white; text-align: center'>Case Study</h2>
                <p style='color: white; text-align: center'>비즈니스 시나리오에 적용해보자!</p>
                <p style='text-align: center'>
                    <a href='https://notion.so' target='_blank'>
                        <button style='background-color: white; color: #3B81F5; padding: 8px 16px; border-radius: 5px; border: none; font-weight: bold; cursor: pointer'>
                            시작하기
                        </button>
                    </a>
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ppt_url = "https://docs.google.com/presentation/d/15cUqztq9yXrbzor0rgyU6jXpH4puvrvY4ZSOcGz6S_s/edit#slide=id.g24035bb5175_0_8"
# st.markdown(f'<iframe src="{ppt_url}" width="800" height="600" frameborder="0" scrolling="no"></iframe>', unsafe_allow_html=True)

####멤버 소개###
st.markdown("---")
st.markdown("""<h2>만든 사람들</h2>""", unsafe_allow_html=True)

<img src="https://github.com/hollyisyoon/streamlit/blob/main/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202023-05-08%20%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE%2011.11.14.png?raw=true"

st.markdown('''   
<div class="team-member">
    <img src="https://media.licdn.com/dms/image/D5603AQGLWfWNmVBIYQ/profile-displayphoto-shrink_800_800/0/1665667362702?e=1689206400&v=beta&t=2RzA1JP0qxRbKImCayGJqEMuFZwZqbTR8QYGLAyz5Rg" class="profile-image">
    <div class="member-info">
        <h3> 윤훈영 </h3>
        <p><code>Product</code> <code>SaaS</code> <code>광고</code> <code>BI</code> 에 관심이 많습니다.
        🚀 매 순간, 끊임없이 성장을 즐기는 사람들과 챌린징한 과제가 있는 환경에서 재밌고 도전적으로 일해보고 싶어요!</p>
        <details>
            <summary><b>Feel Free..</b></summary>
            <p>To Reach Me.. 💙적극 구직 중입니다💙 -> <a id="key" href="https://linkedin.com/in/hoonyoungyoon/" target="_blank">Linkedin</a></p>
        </details>
    </div>
</div>
''', unsafe_allow_html=True)

st.markdown('''   
<div class="team-member">
    <img src="https://media.licdn.com/dms/image/D5603AQGLWfWNmVBIYQ/profile-displayphoto-shrink_800_800/0/1665667362702?e=1689206400&v=beta&t=2RzA1JP0qxRbKImCayGJqEMuFZwZqbTR8QYGLAyz5Rg" class="profile-image">
    <div class="member-info">
        <h3> 김희연 </h3>
        <p>저는 누구냐면요~</p>
        <details>
            <summary><b>More Info</b></summary>
            <p></p>
        </details>
    </div>
</div>
''', unsafe_allow_html=True)

st.markdown('''   
<div class="team-member">
    <img src="https://media.licdn.com/dms/image/D5603AQGLWfWNmVBIYQ/profile-displayphoto-shrink_800_800/0/1665667362702?e=1689206400&v=beta&t=2RzA1JP0qxRbKImCayGJqEMuFZwZqbTR8QYGLAyz5Rg" class="profile-image">
    <div class="member-info">
        <h3> 서인혁 </h3>
        <p>저는 누구냐면요~</p>
        <details>
            <summary><b>More Info</b></summary>
            <p></p>
        </details>
    </div>
</div>
''', unsafe_allow_html=True)

st.markdown('''   
<div class="team-member">
    <img src="https://media.licdn.com/dms/image/D5603AQGLWfWNmVBIYQ/profile-displayphoto-shrink_800_800/0/1665667362702?e=1689206400&v=beta&t=2RzA1JP0qxRbKImCayGJqEMuFZwZqbTR8QYGLAyz5Rg" class="profile-image">
    <div class="member-info">
        <h3> 김효정 </h3>
        <p>저는 누구냐면요~</p>
        <details>
            <summary><b>More Info</b></summary>
            <p></p>
        </details>
    </div>
</div>
''', unsafe_allow_html=True)

st.markdown('''   
<div class="team-member">
    <img src="https://media.licdn.com/dms/image/D5603AQGLWfWNmVBIYQ/profile-displayphoto-shrink_800_800/0/1665667362702?e=1689206400&v=beta&t=2RzA1JP0qxRbKImCayGJqEMuFZwZqbTR8QYGLAyz5Rg" class="profile-image">
    <div class="member-info">
        <h3> 박민정 </h3>
        <p>저는 누구냐면요~</p>
        <details>
            <summary><b>More Info</b></summary>
            <p></p>
        </details>
    </div>
</div>
''', unsafe_allow_html=True)

st.markdown('''   
<div class="team-member">
    <img src="https://media.licdn.com/dms/image/D5603AQGLWfWNmVBIYQ/profile-displayphoto-shrink_800_800/0/1665667362702?e=1689206400&v=beta&t=2RzA1JP0qxRbKImCayGJqEMuFZwZqbTR8QYGLAyz5Rg" class="profile-image">
    <div class="member-info">
        <h3> 송준태 </h3>
        <p>저는 누구냐면요~</p>
        <details>
            <summary><b>More Info</b></summary>
            <p></p>
        </details>
    </div>
</div>
''', unsafe_allow_html=True)

####코멘트###
st.markdown("---")
st.markdown("""<h2>베타 테스터 모집 중</h2>""", unsafe_allow_html=True)