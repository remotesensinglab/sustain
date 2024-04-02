import os
import tempfile
import time
import datetime
import streamlit as st
from streamlit import session_state as sess

from utils import geoprocessing as gp
from utils import planet_backend as pb
from utils import image_processing as ip
from utils import frontend as fend



def app():

    
    # Define the first step pick the date option
    if 'request_date' not in sess:
        date_value = datetime.datetime.now()-datetime.timedelta(days=7)
    else:
        date_value = sess.request_date
    date = fend.step_1_date_pick(date_value)
    sess["request_date"] = date
    date_str = date.strftime("%Y/%m/%d")
    sess['request_date_str'] = date_str
    
    
    # Define the second step pick the range of days to search
    if 'date_range' not in sess:
        date_range_value = 15
    else:
        date_range_value = sess.date_range
    date_range = fend.step_2_date_range(date_range_value)
    sess["date_range"] = date_range
    
    # Draw the map
    st_output = fend.draw_folium_map()
    drawings = st_output["all_drawings"]    
    
    # Check the polygon
    if drawings is None or len(drawings) == 0:
        # Step 3
        fend.step_3_draw_polygon(None)
        # Step 4
        submit_req = fend.step_4_submit_request(True)
        
    else:
        # Get the coordinates from the last drawn polygon
        # and create a geojson geometry
        geojson_geom = {
            "type": "Polygon",
            "coordinates": drawings[-1]['geometry']['coordinates']
            }
        
        # Calculate the area of the drawn polygon
        area = gp.calculate_area(geojson_geom)
        if area > 5:
            # Step 3
            fend.step_3_draw_polygon(area)
            # Step 4
            submit_req = fend.step_4_submit_request(True)
        else:
            sess["aoi_area"] = area
            # Step 3
            fend.step_3_draw_polygon(area)
            # Step 4
            submit_req = fend.step_4_submit_request(False)
            
            if submit_req:
                
                try:
                    # Define the planet engine and search for assets
                    planet_engine = pb.PlanetEngine(
                        geojson_geom, date
                    )
                    image_ids = planet_engine.search_assets(date_range)
                    image_id_date = image_ids[0].split('_')[0][:4]+'/'+image_ids[0].split('_')[0][4:6]+'/'+image_ids[0].split('_')[0][6:]
                    st.sidebar.warning(
                        f"""
                        Based on your search criteria, an image from {image_id_date} is
                        picked.
                        """
                    )
                    sess['image_date'] = image_id_date
                    with st.spinner('Running'):
                                            
                        with tempfile.TemporaryDirectory() as tmpdir:
                            
                            since = time.time()
                            
                            planet_img_path = planet_engine.download_asset(
                                image_ids[0], tmpdir
                            )
                            image_processor = ip.ImageProcessor(
                                planet_img_path, geojson_geom
                            )
                            
                            ndvi = image_processor.ndvi()
                            ndre = image_processor.ndre()
                            
                            image_processor.close_rasterio()
                            
                            sess['image_bounds'] = gp.get_geojson_bounds(
                                geojson_geom
                            )
                            sess['NDVI'] = ndvi
                            sess['NDRE'] = ndre
                                
                            time_elapsed = (time.time()-since)/60.0
                            
                            st.balloons()
                            st.success(
                                f"""
                                Processing finishsed in {time_elapsed:.2f} minutes. Go to
                                `Result` now.
                                """
                            )
                            
                            sess['map_zoom'] = st_output["zoom"]
                            sess['map_lat'] = st_output["center"]["lat"]
                            sess['map_lon'] = st_output["center"]["lng"]
                
                except:
                    st.sidebar.error(
                        f"""
                        Based on your search criteria, no image has been found. Please
                        increase the range of days criteria in Step 2 to widen your
                        search.
                        """
                    )