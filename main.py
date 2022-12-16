import streamlit as st
from pymongo import MongoClient
import pandas as pd
from backend import *
from keys import *

# Establish connection to MongoDB database
client = MongoClient(databaseConnect)
db = client["FundingBase"]
collection = db["Sources"]

# Create the app layout and design
st.title("Funding Sources for Startups")
st.text("This app displays information about different funding sources for startups.")

#sources_found = 0
funding_sources = collection.find({},projection=table_info)

# Button to allow the user to show all funding sources
if st.button("Show all funding sources"):
    # Retrieve data from the database and display it in the app
    funding_sources = collection.find({},projection=table_info)
    #sources_found = 1

# Filter the data by type
with st.expander("Show funding sources by type"):
    # Add input widgets to allow the user to control the app
    funding_type = st.selectbox("Select funding type:", funding_types)
    if st.button("Show funding sources"):
        funding_sources = collection.find({"type": funding_type},projection=table_info)

# Filter the data by city
with st.expander("Show funding sources by city"):
    # Add input widgets to allow the user to control the app
    city = st.selectbox("Select city:", list(collection.distinct("city")))
    if st.button("Show funding sources by city"):
        funding_sources = collection.find({"city": city},projection=table_info)

funding_sources_export = funding_sources.clone()
display_info_table(funding_sources)

col1, col2 = st.columns([1,3.3])
with col1:
    st.write("Export this list to excel:") 

# Export the data to an excel file
outfile = open('output.csv', 'wb')
df = pd.DataFrame(list(funding_sources_export))
df.to_csv(outfile, index=False)
outfile.close()

with col2:
    with open("output.csv", "rb") as file:
        btn = st.download_button(label='Download', data=file, file_name='funding_sources.csv', mime='text/csv')


st.title("Contribute to the database")
with st.expander("Add a new funding source"):
    # Add input widgets for adding new funding source data
    st.title("Add a new funding source")
    name = st.text_input("Name")
    type = st.selectbox("Type", funding_types)
    city = st.selectbox("City", list(collection.distinct("city")))
    city = st.text_input("City")
    amount = st.number_input("Amount", step=1000)
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

with st.expander("Edit funding source data"):
    # Add input widgets for editing funding source data
    name = st.text_input("Name of funding source to edit")
    new_type = st.selectbox("New type ", funding_types)
    new_city = st.selectbox("New city ", list(collection.distinct("city")))
    new_amount = st.number_input("New amount ",step=1000)
    new_requirements = st.text_area("New requirements ")
    new_contact = st.text_input("New contact ")

    # Add a button for submitting the updated data to the database
    if st.button("Edit funding source"):
        # Use the edit_funding_source() function to update the data in the database
        edit_funding_source(collection, name, new_type, new_city, new_amount, new_requirements, new_contact)

st.write("")
st.write("Made by Raphael Leblanc, any contributions are welcome!")
st.write("Github: https://short.raltech.us/r/3pvdW")