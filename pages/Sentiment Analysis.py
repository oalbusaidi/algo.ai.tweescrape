import base64
import streamlit as st
import matplotlib.pyplot as plt
from analysis_services.analysis_services import get_sentiment_results


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

st.write('## Sentiment Analysis Results')
# ------------- Sentiment Analysis ------------------
sentiment = get_sentiment_results()
labels = list(sentiment.keys())
values = list(sentiment.values())

# Create the pie chart using Matplotlib
plt.figure(figsize=(8, 8))  # Adjust the figure size as needed
plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=90, colors=['#8ac926','#ffca3a','#ff595e',])  # Customize options
plt.title("Sentiment Analysis Distribution")

# Display the chart in Streamlit
st.pyplot()

# ------------- Sentiment Analysis ------------------