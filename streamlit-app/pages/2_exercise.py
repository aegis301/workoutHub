import streamlit as st
import plotly.express as px
import pandas as pd
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


# GRAPHS

# total volume per exercise
if st.session_state.sets_per_exercise is not None:
    # if the exercise uses body weight, 80kg are added to the total volume
    if st.session_state.sets_per_exercise["equipment_id"].isna().all():
        st.session_state.sets_per_exercise["weight"] = st.session_state.sets_per_exercise["weight"] + 85
    st.write(st.session_state.sets_per_exercise)
    st.session_state.sets_per_exercise["date"] = pd.to_datetime(st.session_state.sets_per_exercise["date"])
    st.session_state.sets_per_exercise["total_volume"] = st.session_state.sets_per_exercise["weight"] * st.session_state.sets_per_exercise["reps"]  # total volume per set
    # group by date
    sets_by_date = st.session_state.sets_per_exercise.groupby("date").agg(total_volume=("total_volume", "sum")).reset_index()
    fig1 = px.line(
        sets_by_date,
        x="date",
        y="total_volume",
        title="Total Volume per Exercise",
        labels={"total_volume": "Total Volume (kg)"},
    )
    st.plotly_chart(fig1)
