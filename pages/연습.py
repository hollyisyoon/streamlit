import streamlit as st

# Define tabs
tabs = ["식물갤러리", "식물병원", "네이버카페", "네이버블로그", "네이버포스트"]

# Create a sidebar with tab selection
selected_tab = st.sidebar.radio("Tabs", tabs)

# Render content based on selected tab
if selected_tab == "식물갤러리":
    st.write("This is the content of 식물갤러리.")
elif selected_tab == "식물병원":
    st.write("This is the content of 식물병원.")
elif selected_tab == "네이버카페":
    st.write("This is the content of 네이버카페.")
elif selected_tab == "네이버블로그":
    st.write("This is the content of 네이버블로그.")
elif selected_tab == "네이버포스트":
    st.write("This is the content of 네이버포스트.")