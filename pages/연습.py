import streamlit as st

st.write('🙋🏻‍♂️ 바쁜 사람들 멤버를 소개합니다')
html_code = '''
<div class="team-member">
    <img src="https://media.licdn.com/dms/image/D5603AQGLWfWNmVBIYQ/profile-displayphoto-shrink_800_800/0/1665667362702?e=1689206400&v=beta&t=2RzA1JP0qxRbKImCayGJqEMuFZwZqbTR8QYGLAyz5Rg" alt="Profile Image" class="profile-image">
    <div class="member-info">
        <h3 class="name">윤훈영</h3>
        <p class="introduction">안녕하세요오오옹.</p>
    </div>
</div>
'''

css_code = '''
<style>
.team-member {
  display: flex;
  margin-bottom: 20px;
}

.member-info {
  text-align: left;
  margin-left: 10px;
  padding: 20px;
}

.profile-image {
  width: 150px;
  height: 150px;
  border-radius: 50%;
}

.name {
  margin-top: 10px;
  font-size: 20px;
}

.introduction {
  margin-top: 10px;
  font-size: 16px;
}
</style>

'''

st.markdown(css_code, unsafe_allow_html=True)
st.markdown(html_code, unsafe_allow_html=True)

background_image = 'https://publy.imgix.net/images/2022/10/11/1665450720_u3EKEW15vxeIoz6TGBhVwDaFgrO9uMeW6v3BBmEc.png?fm=pjpg'
# Apply background image to parent container
st.markdown(
    f"""
    <style>
        .cta-container-wrapper {{
            display: flex;
            justify-content: center;
            align-items: center;
            background-image: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), url('{background_image}');
            background-size: cover;
            padding: 20px;
            height: 300px;
        }}
    </style>
    """,
    unsafe_allow_html=True
)
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
