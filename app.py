################ Imports ###################
import pandas as pd 
import streamlit as st
import streamlit.components.v1 as components
############################################

interactive_map = open('interactive_map.html','r')
components.html(interactive_map, height = 600)

st.write('Test')