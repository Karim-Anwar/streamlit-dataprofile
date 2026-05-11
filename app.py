
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from ydata_profiling import ProfileReport
import plotly.express as px
import os

# page layout
st.set_page_config(page_title="Data Profiling App", layout="wide")

def validate_file(file):
    if file is not None:
        filename = file.name
        name, ext = os.path.splitext(filename)
        if ext.lower() not in ['.csv', '.xlsx']:
            st.error("Unsupported file type. Please upload a .csv or .xlsx file.")
            return False
        else:
            return ext
    

# Sidebar
sidebar = st.sidebar
with sidebar:
    uploaded_file = st.file_uploader("Upload .csv, .xlsx file not exceeding 10MB", type=["csv", "xlsx"], max_upload_size=10)
    if uploaded_file is not None:
        st.markdown("---")
        st.write("Mode of Operation")
        minimal = st.checkbox("Do you want minimal report?", value=False)
        mode = st.radio("Display mode", options=['Primary', 'Dark', 'Orange'], index=0)
        theme_map = {
            "Primary": "flatly",   # clean light
            "Dark": "cosmo",      # dark mode
            "Orange": "united"     # orange-ish theme
        }


# Main content
st.title("Data Profiling App")
if uploaded_file is not None:
    ext = validate_file(uploaded_file)
    if ext:
        if ext == '.csv':
            df = pd.read_csv(uploaded_file) 
        else:
            df = pd.ExcelFile(uploaded_file)
            sheets = tuple(df.sheet_names)
            sheetname = st.sidebar.selectbox("Select sheet", options=sheets)
            df = df.parse(sheetname)

        # Generate report
        with st.spinner("Generating report..."):
            profile = ProfileReport(df, minimal=minimal, html={'style': {"theme": theme_map[mode]}})
        st.components.v1.html(profile.to_html(), height=2000, scrolling=True)
    else:
        st.error("File validation failed. Please upload a valid .csv or .xlsx file.")
else:
    st.info("Please upload a file to generate the report.")

    