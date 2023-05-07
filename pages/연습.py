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

# <div class="team-member">
#   <div class="member-info">
#     <h3 class="name">Jane Smith</h3>
#     <p class="introduction">Praesent accumsan ligula nec mauris tincidunt, ac volutpat ex condimentum. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae.</p>
#   </div>
#   <img src="profile_image.jpg" alt="Profile Image" class="profile-image">
# </div>
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

cta_container = st.beta_container()
cta_container.markdown(
    """
    <div style='background-color: #f63366; padding: 10px; border-radius: 10px'>
        <h2 style='color: white; text-align: center'>Welcome to my App!</h2>
        <p style='color: white; text-align: center'>Click the button below to get started.</p>
        <p style='text-align: center'>
            <a href='https://your-action-url.com' target='_blank'>
                <button style='background-color: white; color: #f63366; padding: 8px 16px; border-radius: 5px; border: none; font-weight: bold; cursor: pointer'>
                    Get Started
                </button>
            </a>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)