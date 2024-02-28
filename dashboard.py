from analysis_services.analysis_services import (
    clean_tweets_dataframe, get_top_influencers, get_top_locations, get_tweets_per_date,
    get_top_users_replied_to, get_most_common_words_with_counts_nltk,
    get_most_common_words_with_counts_tfidf, get_sentiment_results,
    get_topic_modelling
)
from widgets.user_card import create_twitter_profile_card, user_card_css_style
import matplotlib.pyplot as plt
import sqlite3
import base64
import html
import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
import matplotlib
import folium
from  streamlit_folium import st_folium, folium_static
from geopy.geocoders import Nominatim

matplotlib.use('Agg')


st.set_option('deprecation.showPyplotGlobalUse', False)
st. set_page_config(layout="wide") 

def img_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()




# ------------------- SideBar -----------------------------------
with st.sidebar:
    img_path = "./assets/neural.png"  # Replace with the actual image path
    img_base64 = img_to_base64(img_path)

    st.sidebar.markdown(
        f'<img align="center" src="data:image/png;base64,{img_base64}" width="300">',
        unsafe_allow_html=True,
    )

    # st.write(
    #     """# Topics Searched"""
    # )
    # selected_topics = [topic for topic in [
    #     'Python', 'Data Science', 'Machine Learning', 'Streamlit'] if st.checkbox(topic)]

# ------------------- SideBar -----------------------------------


# ------------------- Main Area -----------------------------------
st.write("""
    # Algo.AI
    ##### Algo.AI is a tool for social media analys  is, that analyzis X platfrom tweets, to get insights about the public opinion about certain topics surrounding an institute.
""")
st.chat_input("Search For a Topic...", key='searchTerm')


col1, col2,  = st.columns(2)


# with col2:


with col1: 
    # ------------- High on Trend Over Time ------------------
    temporal_data = get_tweets_per_date().reset_index()
    st.line_chart(temporal_data, x='date', y=[
                 'likeCount','retweetCount',], color=["rgba(255, 89, 94, 0.5)", "rgba(138, 201, 38, 0.5)", ])
    # ------------- High on Trend Over Time ------------------

with col2:
    # ------------- High on Trend Over Year ------------------
    temporal_data['date'] = pd.to_datetime(temporal_data['date'])
    temporal_data = temporal_data[temporal_data['date'].dt.year == 2023]
    st.line_chart(temporal_data, x='date', y=[
                'likeCount', 'retweetCount', ], color=["rgba(255, 89, 94, 0.5)", "rgba(138, 201, 38, 0.5)", ])
    # ------------- High on Trend Over Year ------------------


with col1:
    # ------------- Top Users Replied to ------------------
    top_replied_to_df = get_top_users_replied_to()
    chart = alt.Chart(top_replied_to_df).mark_bar().encode(
        x=alt.X('username:N', title='Username', sort=None),  # Use index as X-axis
        y=alt.Y('replyCount:Q', title='Reply Count'),
        text='Category:N'
    )
    st.altair_chart(chart, use_container_width=True)
    # ------------- Top Users Replied to ------------------

with col2:
    # ------------- Most Common Words nltk ------------------
    most_common_words = get_most_common_words_with_counts_nltk()

    chart = alt.Chart(most_common_words).mark_bar().encode(
        x=alt.X('topWord:N', title='Word', sort=None),  # Use index as X-axis
        y=alt.Y('wordCount:Q', title='Occurrance'),
    ).configure_axis(labelAngle=35)
    st.altair_chart(chart, use_container_width=True)
    # ------------- Most Common Words nltk ------------------

with col1:
    # ------------- Most Common Words tfidf ------------------

    most_common_words = get_most_common_words_with_counts_tfidf()

    chart = alt.Chart(most_common_words).mark_bar().encode(
        x=alt.X('topWord:N', title='Word', sort=None),  # Use index as X-axis
        y=alt.Y('wordCount:Q', title='Occurrance'),
    ).configure_axis(labelAngle=35)
    st.altair_chart(chart, use_container_width=True)
    # ------------- Most Common Words tfidf ------------------

# with col2:

# ------------- Topic Modelling ------------------
topics_df = get_topic_modelling()
st.dataframe(topics_df, use_container_width=True)
# ------------- Topic Modelling ------------------


# ------------------- Main Area -----------------------------------
