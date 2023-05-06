import streamlit as st
import streamlit.components.v1 as components

st.title("Yellow component")

html_content = "<div>Hello world</div>"
yellow_background = "<style>:root {background-color: yellow;}</style>"
components.html(yellow_background + html_content)