import streamlit as st

STYLE = """
#key {
    color: #000;
    background-color: #FAF3DD;
    text-decoration: none;
}

.name {
    color: f74040;
}

.callout {
    padding: 1em;
    border-radius: 0.5em;
    background-color: #F8F8F8;
    border-left: 4px solid #f74040;
    margin-bottom: 1em;
    color: black;
}

.team-member {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
    border-radius: 10px;
    background-color: #F8F8F8;
    padding: 10px 20px;
    backdrop-filter: blur(5px);
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
    background-image: linear-gradient(rgba(0, 0, 0, 0.2), rgba(0, 0, 0, 0.2)), url('{background_image}');
    background-size: cover;
    padding: 10px;
    height: flex;
    border-radius: 10px;
}
</style>
"""

st.markdown(f"<style>{STYLE}</style>", unsafe_allow_html=True)
st.markdown(f"""
    <h3>📌 바쁜 사람들을 위한 바쁜 사람들 가이드</h3>
    <div class='callout'>
    안녕하세요, 멋사 AI 8기 바쁜 사람들~~~
    </div>""",
    unsafe_allow_html=True
)


####멤버 소개###
st.markdown("---")
st.markdown("""<h3>🙋🏻‍♂️ 만든 사람들</h3>""", unsafe_allow_html=True)

st.markdown('''   
<div class="team-member">
    <img src="https://media.licdn.com/dms/image/D5603AQGLWfWNmVBIYQ/profile-displayphoto-shrink_800_800/0/1665667362702?e=1689206400&v=beta&t=2RzA1JP0qxRbKImCayGJqEMuFZwZqbTR8QYGLAyz5Rg" class="profile-image">
    <div class="member-info">
        <h3 class="name"> 윤훈영(Holly) </h3>
        <p><code>B2B</code> <code>SaaS</code> <code>광고</code> <code>BI</code> 에 관심이 많습니다.
        🚀 매 순간, 끊임없이 성장하는 사람들과 챌린징한 환경에서 재밌고 도전적으로 일해보고 싶어요!</p>
        <details>
            <summary><b>Feel Free..</b></summary>
            <p>To Reach Me.. 💙적극 구직 중입니다💙 <a id="key" href="https://linkedin.com/in/hoonyoungyoon/" target="_blank">Linkedin</a></p>
        </details>
    </div>
</div>
''', unsafe_allow_html=True)

####CTA버튼####
background_image = 'https://publy.imgix.net/images/2022/10/11/1665450720_u3EKEW15vxeIoz6TGBhVwDaFgrO9uMeW6v3BBmEc.png?fm=pjpg'
# Create two CTA containers
cta_container1, cta_container2 = st.beta_columns(2)

# CTA container 1
with cta_container1:
    st.markdown(
        """
        <div class="cta-container-wrapper">
            <div style='padding: 10px; border-radius: 10px'>
                <h2 style='color: white; text-align: center'>사용자 매뉴얼</h2>
                <p style='color: white; text-align: center'>바쁜 사람들이 처음이라면?</p>
                <p style='text-align: center'>
                    <a href='https://notion.so' target='_blank'>
                        <button style='background-color: white; color: #f63366; padding: 8px 16px; border-radius: 5px; border: none; font-weight: bold; cursor: pointer'>
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
        <div class="cta-container-wrapper">
            <div style='padding: 10px; border-radius: 10px'>
                <h2 style='color: white; text-align: center'>사용자 매뉴얼</h2>
                <p style='color: white; text-align: center'>바쁜 사람들이 처음이라면?</p>
                <p style='text-align: center'>
                    <a href='https://notion.so' target='_blank'>
                        <button style='background-color: white; color: #f63366; padding: 8px 16px; border-radius: 5px; border: none; font-weight: bold; cursor: pointer'>
                            살펴보기
                        </button>
                    </a>
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )