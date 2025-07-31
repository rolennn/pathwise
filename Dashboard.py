import streamlit as st
import pandas as pd
from streamlit_timeline import st_timeline

st.set_page_config(layout="centered")

st.write("Dashboard")
with st.expander("Chart"):
	st.write("Chart here!")