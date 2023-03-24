################ Imports ###################
import pandas as pd 
import streamlit as st
import streamlit.components.v1 as components
############################################

def interactive_map():
    st.title('Point of Interest within a given isochrone')
    st.write('This interactive map allows you to draw features and see what points of interest fall within the given polygon, feel free to download the features contained in the polygon once you are done!')
    maps = open('updated.html','r+')
    html = maps.read()
    components.html(html, height = 900)

# Set up the directory for pages in app
pages = {
    "Interactive Map": interactive_map
}

# Create a menu with the page names
selection = st.sidebar.radio("Navigate to:", list(pages.keys()))

# Display the selected page with its corresponding function
pages[selection]()