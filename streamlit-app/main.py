import streamlit as st
import pandas as pd

# Load the data
data = pd.read_csv('data/strong_augmented.csv')

st.title('workoutHub')

# Display the data
st.write(data)
