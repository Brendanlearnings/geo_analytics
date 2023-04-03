################ Imports ###################
import pandas as pd 
import streamlit as st
import streamlit.components.v1 as components
import geocodev2 as gc
import route_planner as rp
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

    address = st.text_input(label='Input the address you would like to geocode',value='4 Waterfall Street, Century City, Cape Town')
    point_on_map = geocode_to_df(address)[0]
    
    st.map(point_on_map)
    st.write('Below is a json object with some interesting information if you would like to expore this specific location on the earth!')
    st.json(geocode_to_df(address)[1], expanded=False)

def route_matrix():
    # Display elements
    construct_df = pd.DataFrame({'Address': []}, dtype=str)
    st.experimental_data_editor(construct_df,num_rows='dynamic',key="data_editor",width=600)
    routes = st.selectbox('What route optimization would you like to use?',
                 ('eco - balance between economy and speed',
                  'fastest - time optimized route',
                  'shortest - utilize the shortest route available'))
    vehicle = st.selectbox('With what vehicle are you traveling with?',
                ('bicycle',
                 'bus',
                 'car',
                 'motorcycle',
                 'pedestrian',
                 'taxi',
                 'truck',
                 'van'))
    traffic = st.selectbox('Would you like to make use of live traffic conditions?',
                 ('Yes',
                  'No'))

    if st.button('Submit'):
        
        data_for_request = construct_df.values.tolist()
        dict_data = st.session_state["data_editor"]
        output_df = pd.DataFrame({'Address': [],
                                  'LATITUDE':[],
                                  'LONGITUDE':[]})
        # Loop through addresses and send a response to the geocoding function.
        for address in dict_data['added_rows']:
            for element in address.values():
                
                get_lat_long = geocode_to_df(str(element))
                lat = get_lat_long[2]
                long = get_lat_long[3]
                construct_data = {
                    'Address': [element],
                    'LATITUDE':[lat],
                    'LONGITUDE':[long]
                }

                insert_df = pd.DataFrame(construct_data)
                output_df = pd.concat([output_df,insert_df],ignore_index=True)

        st.dataframe(output_df,width=600)
        geocoded_points = output_df[['LATITUDE','LONGITUDE']].values.tolist()
        st.map(output_df)

        # Map inputs to package request parameters
        if routes == 'eco - balance between economy and speed':
            route = 'eco'
        if routes == 'fastest - time optimized route':
            route = 'fastest'
        if routes == 'shortest - utilize the shortest route available':
            route = 'shortest'
        
        if traffic == 'Yes':
            traf = 'true'
        else:
            traf = 'false'

        route_plan = rp.route_matrix(points=geocoded_points,avoid=[],departAt=None,RouteType=route,travelMode=vehicle,traffic=traf)
        st.json(route_plan)
        route_data = route_plan["routes"][0]["legs"][0]["points"]
        st.json(route_data)
        

# ################################


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