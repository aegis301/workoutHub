import streamlit as st
import pandas as pd
import requests


def convert_response_data_to_df(response_data):
    data = response_data.json()
    df = pd.DataFrame(data)
    return df


# get the data from the server
sets_response = requests.get('http://localhost:8000/sets/')

sets = convert_response_data_to_df(sets_response)

st.title('workoutHub')

# Display the data
st.write(sets)

st.header("Exercise Count by Primary Muscle Group per Week")
primary_muscle_group_response = requests.get('http://localhost:8000/sets/primary_muscle_group/Back')
sets_by_primary_muscle_group = convert_response_data_to_df(primary_muscle_group_response)
# group by week
# coearce the date to datetime
sets_by_primary_muscle_group["date"] = pd.to_datetime(sets_by_primary_muscle_group["date"])
# extract both year and week number to avoid grouping different years together
sets_by_primary_muscle_group["year"] = sets_by_primary_muscle_group["date"].dt.year
sets_by_primary_muscle_group["week"] = sets_by_primary_muscle_group["date"].dt.isocalendar().week

# group by both year and week
sets_by_primary_muscle_group_by_week = sets_by_primary_muscle_group.groupby(["year", "week"])["exercise_id"].count().reset_index()

# Display the grouped data
st.write(sets_by_primary_muscle_group_by_week)
st.line_chart(sets_by_primary_muscle_group_by_week, y="exercise_id")