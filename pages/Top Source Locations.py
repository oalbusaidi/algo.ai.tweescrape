import base64
import folium
import streamlit as st
from geopy.geocoders import Nominatim
from streamlit_folium import folium_static
from analysis_services.analysis_services import get_top_locations


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

# ------------- Top Locations ------------------
st.write('## Top Source Locations')
top_locations_series = get_top_locations()


data = top_locations_series.to_frame(name='value').reset_index(names=['Location'])

oman_map = folium.Map(location=[23.6100, 58.5900], zoom_start=5)
geolocator = Nominatim(user_agent="my_app")
for location in data['Location']:
        try:
            print("location", location)
            if location.strip():
                location = geolocator.geocode(location)
                coordinates = (location.latitude, location.longitude)
                # folium.Marker(location=coordinates).add_to(oman_map)
                folium.CircleMarker(
                     location=coordinates,
                     radius=1000,
                     color='red',
                    fill_color='red',
                    # fill_opacity=0.4,
                    tooltip=f"Interaction: {data[data['Location'] == location]['value']}" 
                ).add_to(oman_map)
        except :
            print('Couldn\'t find location' )
            continue

folium_static(oman_map, width=1000)
    # st.write(oman_map, unsafe_allow_html=True)
    # chart = alt.Chart(data).mark_bar().encode(
    #     x=alt.X('Location:N', title='Location', sort=None),  # Use index as X-axis
    #     y=alt.Y('value:Q', title='Tweet Count'),
    #     text='Location:N'
    # )

    # st.altair_chart(chart, use_container_width=True)
    # ------------- Top Locations ------------------