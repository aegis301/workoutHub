import streamlit as st
from utils import query_with_cache

st.set_page_config(
    page_title="Exercise",
    page_icon="🏋️",
)

st.title("Exercise")

exercises = query_with_cache('http://localhost:8000/exercises/')
equipment = query_with_cache('http://localhost:8000/equipment/')

if "sets_per_exercise" not in st.session_state:
    st.session_state.sets_per_exercise = {}


def query_exercise(e_selection, eq_selection):
    if e_selection is None:
        st.warning("Please select an exercise.")
        return {}
    st.session_state.exercise_selection = e_selection
    # find exercise id
    exercise_option = exercises[exercises.name == e_selection].id.values[0]

    if eq_selection != "All":
        equipment_option = equipment[equipment.name == eq_selection].id.values[0]
        query = f"http://localhost:8000/sets/exercises/equipment/{exercise_option}/{equipment_option}"
    else:
        query = f'http://localhost:8000/sets/exercises/{exercise_option}'
    if exercise_option not in st.session_state.sets_per_exercise:
        st.session_state.sets_per_exercise = query_with_cache(query)
    return st.session_state.sets_per_exercise


with st.form(key="exercise_form"):
    exercise_selection = st.selectbox(
        "Exercise",
        exercises.name if exercises is not None else [],
        index=None,
        placeholder="Select an exercise...",
    )
    equipment_options = ["All"] + (equipment.name.tolist() if equipment is not None else [])
    equipment_selection = st.selectbox(
        "Equipment",
        equipment_options,
        index=0,
        placeholder="Select an equipment...",
    )
    submit_button = st.form_submit_button(label="Submit")


if submit_button:
    sets = query_exercise(exercise_selection, equipment_selection)
    st.write(st.session_state.sets_per_exercise)
