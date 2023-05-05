import streamlit as st
from annotated_text import annotated_text

annotated_text(
    "This ",
    ("일장", "1"),
    " some ",
    ("annotated", "adj"),
    ("text", "noun"),
    " for those of ",
    ("you", "pronoun"),
    " who ",
    ("like", "verb"),
    " this sort of ",
    ("thing", "noun"),
    "."
)