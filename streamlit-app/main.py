import streamlit as st
import pandas as pd
import requests


# get the data from the server
sets_response = requests.get('http://localhost:8000/sets/')
# convert to pandas dataframe
data = sets_response.json()
data = pd.DataFrame(data)

st.title('workoutHub')

# Display the data
st.write(data)

