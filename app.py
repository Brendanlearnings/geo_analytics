################ Imports ###################
import pandas as pd 
import streamlit as st
import streamlit.components.v1 as components
############################################

def interactive_map():
    st.title('Testing the download functionality after making a selection')
    maps = open('updated.html','r+')
    html = maps.read()
    components.html(html, height = 900)

# Set up the directory for pages in app
pages = {
    "Interactive Map": interactive_map
}

# Create a menu with the page names
selection = st.sidebar.radio("Go to", list(pages.keys()))

# Display the selected page with its corresponding function
pages[selection]()