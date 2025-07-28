import streamlit as st
from streamlit_timeline import st_timeline
import pandas as pd

st.set_page_config(layout="wide")

items = [
	{"id": 1, "content": "Education", "start": "2022-10-20"},
	{"id": 2, "content": "Savings", "start": "2022-10-09"},
	{"id": 3, "content": "Marriage", "start": "2022-10-18"},
	{"id": 4, "content": "House", "start": "2022-10-16"},
	{"id": 5, "content": "Vehicle", "start": "2022-10-25"},
]

timeline = st_timeline(items, groups=[], options={}, height="300px")
st.subheader("Selected item")
st.write(timeline)
