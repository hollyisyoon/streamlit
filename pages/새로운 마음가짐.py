import pandas as pd
import koreanize_matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.colors import to_rgba
import plotly.graph_objects as go
import plotly.express as px
import ast
import time

import streamlit as st
from streamlit_extras.let_it_rain import rain

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from collections import Counter
from wordcloud import WordCloud
from datetime import datetime, timedelta

import warnings
warnings.filterwarnings("ignore", message="PyplotGlobalUseWarning")
import networkx as nx
from gensim.models import Word2Vec
import time

rain(emoji="🦝",
    font_size=54,
    falling_speed=10,
    animation_length="infinite")

df = pd.read_csv('/app/streamlit/data/df_트렌드_github.csv', encoding='utf8')
df['time'] = pd.to_datetime(df['time'])

print(df)

