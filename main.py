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

funding_sources = collection.find({},projection={"_id": False,"name": 1, "type": 1, "amount":1 , "city": 1, "requirements": 1, "contact": 1})

with st.expander("Show funding sources by type"):
    # Add input widgets to allow the user to control the app
    funding_type = st.selectbox("Select funding type:", ["seed", "venture", "angel", "bursary", "grant", "loan", "equity", "other"])
    if st.button("Show funding sources"):
        # Retrieve data from the database and display it in the app
        funding_sources = collection.find({"type": funding_type},projection={"_id": False,"name": 1, "type": 1,"amount":1 , "city": 1, "requirements": 1, "contact": 1})
        

with st.expander("Show funding sources by city"):
    # Add input widgets to allow the user to control the app
    city = st.selectbox("Select city:", list(collection.distinct("city")))
    if st.button("Show funding sources by city"):
        # Retrieve data from the database and display it in the app
        funding_sources = collection.find({"city": city},projection={"_id": False,"name": 1, "type": 1, "amount":1 ,"city": 1, "requirements": 1, "contact": 1})

display_info_table(funding_sources)

#st.write("Export this list to excel:") # I cannot get this to work 
#if st.button("Export to excel"):
    # Export the data to an excel file
    #outfile = open('output.csv', 'wb')
    #df = pd.DataFrame(dtype=int)
    #df.to_csv(outfile, index=False)
    #outfile.close()
    #download the excel file
    #st.markdown(get_table_download_link(df), unsafe_allow_html=True)

st.title("Contribute to the database")
with st.expander("Add a new funding source"):
    # Add input widgets for adding new funding source data
    st.title("Add a new funding source")
    name = st.text_input("Name")
    type = st.selectbox("Type", ["seed", "venture", "angel", "bursary", "grant", "loan", "equity", "other"])
    city = st.selectbox("City", list(collection.distinct("city")))
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
    new_type = st.selectbox("New type ", ["seed", "venture", "angel", "bursary", "grant", "loan", "equity", "other"])
    new_city = st.selectbox("New city ", list(collection.distinct("city")))
    new_amount = st.number_input("New amount ")
    new_requirements = st.text_area("New requirements ")
    new_contact = st.text_input("New contact ")

    # Add a button for submitting the updated data to the database
    if st.button("Edit funding source"):
        # Use the edit_funding_source() function to update the data in the database
        edit_funding_source(collection, name, new_type, new_city, new_amount, new_requirements, new_contact)