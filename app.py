################ Imports ###################
import pandas as pd 
import streamlit as st
import streamlit.components.v1 as components
############################################

interactive_map = open('interactive_map.html','r')
html = interactive_map.read()
components.html(html, height = 600)

st.write('Test')