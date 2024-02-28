import base64
import sqlite3
import pandas as pd
import streamlit as st
from widgets.user_card import create_twitter_profile_card, user_card_css_style
from analysis_services.analysis_services import get_top_influencers



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
    

st.write('## Top Influencers')
col1, col2, col3 , col4 = st.columns(4)

# --------- Top Influencers -------------------
st.write(user_card_css_style, unsafe_allow_html=True)
top_influencers = get_top_influencers()
if not top_influencers.empty:
    connection = sqlite3.connect('scraping_services/scraped_data.db')
    user_df = pd.read_sql_query("SELECT * from twitter_user", connection)
    # Merge with userdf to get usernames
    top_influencers_with_username = pd.merge(top_influencers, user_df, on='userid', how='left')
    count = 0
    for index, row in top_influencers_with_username.iterrows():
        username = row['username_x']
        influenceScore = row['influenceScore']
        if count % 3 == 0:
            col = col1
        elif count % 3 == 1:
            col = col2
        elif count % 3 == 2:
            col = col3
        with col:
            st.markdown(create_twitter_profile_card(username, influenceScore, count + 1), unsafe_allow_html=True)
        count += 1 
#         # Visualize the top influencers using Altair in Streamlit
#         chart = alt.Chart(top_influencers_with_username).mark_bar().encode(
#             y=alt.Y('influenceScore:Q', title='Influence Score', sort=None),
#             x=alt.X('username_x:O', title='Username', sort='y'),
#         ).properties(
#             width=500,
#             title='Top Influencers'
#         )

#         # Display Altair chart in Streamlit
#         st.altair_chart(chart, use_container_width=True)
#     else:
#         st.write("No data available for plotting.")
#     # ------------- Top Influencers ------------------