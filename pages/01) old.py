import pyperclip
import streamlit as st

text_to_copy = "Hello, Streamlit!"

if st.button("Copy to Clipboard"):
    pyperclip.copy(text_to_copy)
    st.success("Text copied to clipboard!")
