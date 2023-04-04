################ Imports ###################
import pandas as pd 
import streamlit as st
import streamlit.components.v1 as components
import geocodev2 as gc
import route_planner as rp
import pydeck as pdk
import random
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

def random_color_generator():
    chars = '0123456789ABCDEF'

    return '#'+''.join(random.sample(chars,6))

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
    st.title('Route Optimization')
    st.markdown('This module is intended to optimize a route with `x` amount of waypoints (up to 150 can be used).')
    st.markdown('Please enter the fully qualified addresses that you would like to use.')
    st.markdown('* The first address is the starting.')
    st.markdown('* The last address is the destination')
    st.markdown('* The waypoints can be ordered however you like, the module will determine the most efficient between them.')

    # Input elements
    construct_df = pd.DataFrame({'Address': []}, dtype=str)
    st.experimental_data_editor(construct_df,num_rows='dynamic',key="data_editor",use_container_width=True)
    st.markdown('Please select the options you would like to use in the module.')
    routes = st.selectbox('What route optimization would you like to use?',
                 ('eco - balance between economy and speed',
                  'fastest - time optimized route',
                  'shortest - utilize the shortest route available'))
    vehicle = st.selectbox('With what vehicle are you traveling with?',
                ('car',
                 'bicycle',
                 'bus',
                 'motorcycle',
                 'pedestrian',
                 'taxi',
                 'truck',
                 'van'))
    traffic = st.selectbox('Would you like to make use of live traffic conditions?',
                 ('Yes',
                  'No'))

    # Display the output for the given input parameters
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

        geocoded_points = output_df[['LATITUDE','LONGITUDE']].values.tolist()
        st.write('This is a representation of the start, end and waypoints.')
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
        # Create an empty json object to append points into 
        data_points_for_route = {}
        address_list = output_df['Address'].values.tolist()
        for address in range(len(output_df['Address'].values.tolist())-1):
            name = address
            data = {'name':[f"{address_list[address]} - {address_list[address+1]}"],
                    'color':[random_color_generator()],
                    'path':[[points for points in route_plan['routes'][0]['legs']]]}
            data_points_for_route.update(data)
            
        st.json(data_points_for_route)

        # route_plan['routes'][0]['legs']
        # Loop through the response and extract all data that is associated with points:
        # for route_points in route_plan["routes"]:
        #     for leg in route_points['legs']:
        #         print(leg['points'])
        #         for points in leg['points']:
        #             data_points_for_route.append(points)
        # Display route as a collection of points -- should udpate this to be a line instead of collection of points. 
        # st.write('Your optimized route!')
        # route_points = pd.json_normalize(data_points_for_route)
        # st.map(route_points)

        # process_json_total_travel = route_plan['routes'][0]['summary']
        # json_total_travel = {'Address':['Total'],
        #                     'TravelTimeHoursNoTraffic': [(process_json_total_travel['noTrafficTravelTimeInSeconds'])/60/60],
        #                     'TravelTimeHoursHistorical': [(process_json_total_travel['historicTrafficTravelTimeInSeconds'])/60/60],
        #                     'TravelTimeHoursLiveTraffic': [(process_json_total_travel['liveTrafficIncidentsTravelTimeInSeconds'])/60/60],
        #                     'TravelDistanceKM': [(process_json_total_travel['lengthInMeters'])/1000],
        #                      'DepartureTime': [process_json_total_travel['departureTime']],
        #                      'ArrivalTime': [process_json_total_travel['arrivalTime']]
        # }
        
        
        # travel_metadata_df = pd.DataFrame(json_total_travel)
        # st.dataframe(travel_metadata_df,use_container_width=True)

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