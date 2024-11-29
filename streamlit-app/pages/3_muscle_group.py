import streamlit as st
import pandas as pd
from utils import query_with_cache
st.set_page_config(
    page_title="Muscle Group",
    page_icon="💪🏼",
)

st.title("Muscle Group")
st.write("This is a placeholder for the muscle group page.")


muscle_groups = query_with_cache('http://localhost:8000/muscle-groups/')

if "sets_per_muscle_group" not in st.session_state:
    st.session_state.sets_per_muscle_group = pd.DataFrame()


def query_muscle_group(mg_selection):
    if mg_selection is None:
        st.warning("Please select a muscle group.")
        return {}
    st.session_state.muscle_group_selection = mg_selection
    # find muscle group id
    for mg in mg_selection:
        new_data = query_with_cache(f'http://localhost:8000/sets/primary-muscle-group/{mg}')
        st.session_state.sets_per_muscle_group = pd.concat(
            [st.session_state.sets_per_muscle_group, new_data], ignore_index=True
        )
    return st.session_state.sets_per_muscle_group


st.write(muscle_groups)

with st.form(key="muscle_group_form"):
    muscle_group_selection = st.multiselect(
        "Muscle Group",
        muscle_groups.name if muscle_groups is not None else [],
        placeholder="Select a muscle group...",
    )
    submit_button = st.form_submit_button(label="Submit")

if submit_button:
    sets = query_muscle_group(muscle_group_selection)
    st.write(sets)
