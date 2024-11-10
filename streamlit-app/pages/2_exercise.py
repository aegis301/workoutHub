import streamlit as st
from utils import query_with_cache

st.set_page_config(
    page_title="Exercise",
    page_icon="🏋️",
)

st.title("Exercise")

exercises = query_with_cache('http://localhost:8000/exercises/')

if "sets_per_exercise" not in st.session_state:
    st.session_state.sets_per_exercise = {}


def query_exercise(option):
    if option is None:
        st.warning("Please select an exercise.")
        return {}
    if option not in st.session_state.sets_per_exercise:
        st.session_state.sets_per_exercise[option] = query_with_cache('http://localhost:8000/exercises/' + option)
    return st.session_state.sets_per_exercise[option]


with st.form(key="exercise_form"):
    option = st.selectbox(
        "Exercise",
        exercises.name.values if exercises is not None else [],
        index=None,
        placeholder="Select an exercise...",
    )

    if st.form_submit_button("Submit"):
        query_exercise(option)

st.write(st.session_state.sets_per_exercise)
