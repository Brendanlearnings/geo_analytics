################ Imports ###################
import pandas as pd 
import streamlit as st
import streamlit.components.v1 as components
import geocodev2 as gc
############################################

####### Fucntions for reuse ####
def geocode_to_df(location):
    '''This function takes the response from the azure maps geocode and extracts the location as a dataframe and json object for reuse'''
    # Data retrieval and manipulation elements 
    all_data_from_response = gc.geocode(location)
    lat = all_data_from_response['results'][0]['position']['lat']
    long = all_data_from_response['results'][0]['position']['lon']

    # Prep and display retrived data
    map_data = {
        'LATITUDE':[lat],
        'LONGITUDE':[long]
    }
    map_df = pd.DataFrame(map_data)

    return map_df,all_data_from_response
################################
####### App Pages ###########
def interactive_map():
    st.title('Point of Interest within a given isochrone')
    st.write('This interactive map allows you to draw features and see what points of interest fall within the given polygon, feel free to download the features contained in the polygon once you are done!')
    st.write('Please note that one a new POI Query is typed that you need to redraw the polygon')
    maps = open('updated.html','r+')
    html = maps.read()
    components.html(html, height = 700)

def geocode():
    # Display elements
    st.title('Geocode a address to a extract some usefull information from it.')
    address = st.text_input('Fully qualified address (eg. 4 Waterfall Street, Century City, Cape Town)', value='4 Waterfall Street, Century City, Cape Town', label_visibility='hidden')
    point_on_map = geocode_to_df(address)[0]
    
    st.map(point_on_map)
    st.json(geocode_to_df(address)[1], expanded=False)
################################


# Set up the directory for pages in app
pages = {
    "Interactive Map": interactive_map,
    "Geocode": geocode
}

# Create a menu with the page names
selection = st.sidebar.radio("Navigate to:", list(pages.keys()))

# Display the selected page with its corresponding function
pages[selection]()