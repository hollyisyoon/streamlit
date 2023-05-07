import streamlit as st

html_code = '''
<div class="team-member">
  <img src="profile_image.jpg" alt="Profile Image" class="profile-image">
  <h3 class="name">John Doe</h3>
  <p class="introduction">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed vitae libero velit. Proin commodo vestibulum arcu. Nullam eu est nulla.</p>
</div>

<div class="team-member">
  <img src="profile_image.jpg" alt="Profile Image" class="profile-image">
  <h3 class="name">Jane Smith</h3>
  <p class="introduction">Praesent accumsan ligula nec mauris tincidunt, ac volutpat ex condimentum. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae.</p>
</div>
'''

css_code = '''
<style>
.team-member {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  margin-bottom: 20px;
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
