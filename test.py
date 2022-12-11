# Import the necessary libraries
import pandas as pd
import streamlit as st

# Create a sample dataframe
df = pd.DataFrame({'my_string': ['this, is, a, sample, string']})

# Replace the commas with bullet points
df['my_string'] = df['my_string'].str.replace(',', '\n •')

# Display the dataframe in a table
st.dataframe(df)
