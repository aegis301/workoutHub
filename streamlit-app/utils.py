import msgpack
import pandas as pd
import requests
import streamlit as st


@st.cache_data(show_spinner=False)
def query_with_cache(api_url):
    response = None
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Debug: Check if we're actually getting MessagePack
        content_type = response.headers.get('content-type', '')
        
        if 'application/msgpack' in content_type:
            # Try to unpack MessagePack data
            response_json = msgpack.unpackb(response.content, raw=False)
            return pd.DataFrame(response_json)
        else:
            # Fallback to JSON if not MessagePack
            st.warning(f"Expected MessagePack but got: {content_type}. Trying JSON fallback.")
            response_json = response.json()
            return pd.DataFrame(response_json)
        
    except msgpack.exceptions.ExtraData as e:
        st.error(f"MessagePack parsing error: {e}")
        if response:
            st.error(f"Response headers: {dict(response.headers)}")
            st.error(f"Response content (first 200 bytes): {response.content[:200]}")
        
        # Try JSON fallback
        try:
            if response:
                st.info("Attempting JSON fallback...")
                response_json = response.json()
                return pd.DataFrame(response_json)
            else:
                return pd.DataFrame()
        except Exception:
            st.error("JSON fallback also failed")
            return pd.DataFrame()
            
    except requests.exceptions.RequestException as e:
        st.error(f"HTTP request failed: {e}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        if response:
            st.error(f"Response content: {response.content[:200]}")
        return pd.DataFrame()
