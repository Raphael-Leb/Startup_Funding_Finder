import streamlit as st
from pymongo import MongoClient
import pandas as pd
from backend import *

# Establish connection to MongoDB database
client = MongoClient("mongodb://raphael:startup@96.22.162.234:27018/?authMechanism=DEFAULT&authSource=FundingBase")
db = client["FundingBase"]
collection = db["Sources"]

# Create the app layout and design
st.title("Funding Sources for Startups")
st.text("This app displays information about different funding sources for startups.")

funding_sources = collection.find({},projection={"_id": False,"name": 1, "type": 1, "city": 1, "requirements": 1, "contact": 1})

with st.expander("Show funding sources by type"):
    # Add input widgets to allow the user to control the app
    funding_type = st.selectbox("Select funding type:", ["seed", "venture", "angel", "bursary", "grant", "loan", "equity", "other"])
    if st.button("Show funding sources"):
        # Retrieve data from the database and display it in the app
        funding_sources = collection.find({"type": funding_type},projection={"_id": False,"name": 1, "type": 1, "city": 1, "requirements": 1, "contact": 1})
        

with st.expander("Show funding sources by city"):
    # Add input widgets to allow the user to control the app
    city = st.selectbox("Select city:", list(collection.distinct("city")))
    if st.button("Show funding sources by city"):
        # Retrieve data from the database and display it in the app
        funding_sources = collection.find({"city": city},projection={"_id": False,"name": 1, "type": 1, "city": 1, "requirements": 1, "contact": 1})

st.table(funding_sources)

st.title("Contribute to the database")
with st.expander("Add a new funding source"):
    # Add input widgets for adding new funding source data
    st.title("Add a new funding source")
    name = st.text_input("Name")
    type = st.selectbox("Type", ["seed", "venture", "angel", "bursary", "grant", "loan", "equity", "other"])
    city = st.selectbox("City", list(collection.distinct("city")))
    amount = st.number_input("Amount")
    requirements = st.text_area("requirements")
    contact = st.text_input("Contact")

    # Add a button for submitting the new data to the database
    if st.button("Add funding source"):
        # Use PyMongo to add the new funding source data to the database
        result = collection.insert_one({
            "name": name,
            "type": type,
            "city": city,
            "amount": amount,
            "requirements": requirements,
            "contact": contact
        })
        st.write("Added funding source with id:", result.inserted_id)