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

    # Prep data into dataframe that is excessable through the st.maps element
    map_data = {
        'LATITUDE':[lat],
        'LONGITUDE':[long]
    }
    map_df = pd.DataFrame(map_data)

    return map_df,all_data_from_response,lat,long
################################
####### App Pages ###########
def interactive_map():
    st.title('Point of Interest within a given isochrone')
    st.markdown('This interactive map allows you to draw features and see what points of interest fall within the given polygon.')
    st.write('Please note that one a new POI Query is typed that you need to redraw the polygon')
    maps = open('updated.html','r+')
    html = maps.read()
    components.html(html, height = 700)

def geocode():
    # Display elements
    st.title('Geocode an address or point of interest to a extract some usefull information from it.')

    address = st.text_input(value='4 Waterfall Street, Century City, Cape Town', label_visibility='hidden')
    point_on_map = geocode_to_df(address)[0]
    
    st.map(point_on_map)
    st.write('Below is a json object with some interesting information if you would like to expore this specific location on the earth!')
    st.json(geocode_to_df(address)[1], expanded=False)

def route_matrix():
    # Display elements
    construct_df = pd.DataFrame({'Address': ['Please enter the address you would like to use']}, dtype=str)
    st.experimental_data_editor(construct_df,num_rows='dynamic')

    if st.button('Submit'):
        construct_df['Lattitude'] = geocode_to_df(construct_df['Address'])[2]
        construct_df['Longitude'] = geocode_to_df(construct_df['Address'])[3]

        st.dataframe(data=construct_df)
################################


# Set up the directory for pages in app
pages = {
    "Interactive Map": interactive_map,
    "Geocode": geocode,
    "Route Optimization": route_matrix
}

# Create a menu with the page names
selection = st.sidebar.radio("Navigate to:", list(pages.keys()))

# Display the selected page with its corresponding function
pages[selection]()