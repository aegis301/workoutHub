import msgpack
import pandas as pd
import streamlit as st
import requests


@st.cache_data(show_spinner=False)
def query_with_cache(api_url):
    response = requests.get(api_url)
    response_json = msgpack.unpackb(response.content, raw=False)
    return pd.DataFrame(response_json)
