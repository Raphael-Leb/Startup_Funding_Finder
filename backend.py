import streamlit as st
from pymongo import MongoClient
import pandas as pd

def display_info_table(funding_sources):
    #st.dataframe(funding_sources[["name", "type", "city", "requirements", "contact"]]) 
    st.table(funding_sources)