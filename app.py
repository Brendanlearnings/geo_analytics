################ Imports ###################
import pandas as pd 
import streamlit as st
import streamlit.components.v1 as components
############################################
def interactive_map():
    st.title('Interactive Map')
    st.write('Feel free to play around with the map and draw whatever features you would like to draw')
    interactive_map = open('interactive_map.html','r')
    html = interactive_map.read()
    components.html(html, height = 600)

def test_page():
    st.write('This is a test page')
    download = open('test_download.html','r')
    html = download.read()
    components.html(html)

def test_download():
    st.title('Testing the download functionality after making a selection')
    maps = open('updated.html','r+')
    html = maps.read()
    components.html(html, height = 900)

# Set up the directory for pages in app
pages = {
    "Interactive Map": interactive_map,
    "TEST": test_page,
    "Updated":test_download
}

# Create a menu with the page names
selection = st.sidebar.radio("Go to", list(pages.keys()))

# Display the selected page with its corresponding function
pages[selection]()