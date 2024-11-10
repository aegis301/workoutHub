import streamlit as st
from utils import query_with_cache

st.set_page_config(
    page_title="Exercise",
    page_icon="🏋️",
)

st.title("Exercise")

exercises = query_with_cache('http://localhost:8000/exercises/')


with st.form(key="exercise_form"):
    option = st.selectbox(
        "Exercise",
        exercises.name.values,
        index=None,
        placeholder="Select an exercise...",
    )
    st.form_submit_button(label="Submit")
