import streamlit as st
from pymongo import MongoClient
from pymongo.collection import Collection
import pandas as pd

funding_types = ["seed", "venture", "angel", "incubator", "bursary", "grant", "loan", "equity", "subsidy" ,"other"]
table_info = {"_id": False,"name": 1, "type": 1,"amount":1 , "city": 1, "requirements": 1, "contact": 1}

def display_info_table(funding_sources):
    empty_check = funding_sources.clone()
    count = len(list(empty_check))
    if count == 0:
        st.write("No funding sources found")
    else:
        #create a pandas dataframe from the list of funding sources
        df = pd.DataFrame(funding_sources)

        #change the order of the columns
        df = df[["name", "type", "amount", "city", "requirements", "contact"]]

        #rename the columns
        df.columns = ["Name", "Type", "Amount", "City", "Requirements", "Contact"]

        #Make bullet lists for the requirements column
        #insert a bullet point before each entry
        #df['Requirements'] = df['Requirements'].str.replace(',', '\n •') # I cannot get this to work please help

        #display the dataframe as a table
        st.table(df.style.format({"Amount": "{:,.0f}"}))

def edit_funding_source(collection, name, new_type, new_city, new_amount, new_requirements, new_contact):
    # Retrieve the funding source document that needs to be updated
    funding_source = collection.find_one({"name": name})

    # Update the values for the fields in the document
    result = collection.update_one(
        {"name": name},
        {
            "$set": {
                "type": new_type,
                "city": new_city,
                "amount": new_amount,
                "requirements": new_requirements,
                "contact": new_contact
            }
        }
    )

    # Print the number of documents that were updated
    st.write("Number of documents updated:", result.modified_count)
    if result.modified_count == 0:
        st.write("Funding source failed to be edited, did you write the name correctly?")