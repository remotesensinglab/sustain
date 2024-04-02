import os
import streamlit as st
import datetime
import folium
from dotenv import load_dotenv
from streamlit_folium import st_folium

# Load the environment variable
load_dotenv(".env")


def draw_folium_map():
    
    # Mapbox API
    MAPBOX_KEY = ("pk.eyJ1Ijoic2JoYWRyYSIsImEiOiJjbGR0cmQ2djIwN21mM3RveHFzdmo3a3JzIn0.Udsy1WalxEv0QBhtVlmHwg")
    tileset_ID_str = "satellite-streets-v12"
    mapbox_tile_URL = f"https://api.mapbox.com/styles/v1/mapbox/{tileset_ID_str}/tiles/{{z}}/{{x}}/{{y}}@2x?access_token={MAPBOX_KEY}"
    
    # Deine geometries for map visualization
    if 'map_zoom' not in st.session_state:
        map_zoom = 4
    else:
        map_zoom = st.session_state.map_zoom
    if 'map_lat' not in st.session_state:
        map_lat = 39
    else:
        map_lat = st.session_state.map_lat
    if 'map_lon' not in st.session_state:
        map_lon = -100
    else:
        map_lon = st.session_state.map_lon
        
    # Draw the map
    m = folium.Map(
        location=[map_lat, map_lon], #[39, -100]
        zoom_start=map_zoom,
        tiles=mapbox_tile_URL,
        attr='Mapbox'
    )
    
    folium.plugins.Geocoder().add_to(m)
    folium.plugins.Draw(
        draw_options={
            'polyline': False,
            'polygon': False,
            'circle': False,
            'marker': False,
            'circlemarker': False
        }
    ).add_to(m)
    
    output = st_folium(
        m,
        width='100%', 
        height=600
    )
    
    return output


def step_1_date_pick(
    date
):
    
    help_message = """
    The selectable date is 7 days prior to current date as you cannot pick a very recent
    date.
    """
    maximum_date = datetime.datetime.now()-datetime.timedelta(days=7)
    minimum_date = datetime.date(2022, 1, 1)
    date = st.sidebar.date_input(
        label="Step 1: Select date",
        value=date,
        min_value=minimum_date,
        max_value=maximum_date,
        help=help_message
    )

    return date


def step_2_date_range(
    date_range_value
):
    help_message = """
    By default the range is 15 days. The system will search image assets between your
    selected date and the number of days specified here from the selected date.
    """
    date_range = st.sidebar.slider(
        label='Step 2: Number of days prior to selecetd date',
        min_value=1,
        max_value=30,
        value=date_range_value,
        help=help_message
    )
    return date_range


def step_3_draw_polygon(area):
    """
    The stage can be ["initial", "large_area", "correct"]
    """
    st.sidebar.markdown(
        "<p style='font-size: 13.5px'>Step 3: Define a valid polygon</p>",
        unsafe_allow_html=True
    )
    if area==None:
        st.sidebar.warning(
            """
            Draw a polygon using the ⬛ button on the left pan of map. The polygon should
            be less than 5 Sq Km or 1235 acres
            """
        )
    elif area > 5:
        st.sidebar.error(
            f"""
            The polygon is {area:.2f} Sq Km, it has to be less than 5 Sq Km or 1235 acres
            """
        )
    elif area < 5:
        st.sidebar.success(
            f"""
            Your polygon of {area:.2f} Sq Km is valid
            """
        )
        
    
def step_4_submit_request(
    disabled=True
):
    
    # Add the html header
    write_heading_as_html(
        "Step 4: Submit request (can take 15-20 minutes)"
    )
    if disabled:
        help_message = """
        Complete previous steps to perform this operation
        """
    else:
        help_message = """
        Might take 15/20 minute, do not close browser
        """
    # Add the button
    submit_req = st.sidebar.button(
        label='Submit Request',
        help=help_message,
        disabled=disabled
    )
    return submit_req
    


def write_heading_as_html(
    label
):
    st.sidebar.markdown(
        f"<p style='font-size: 13.5px'>{label}</p>",
        unsafe_allow_html=True
    )
