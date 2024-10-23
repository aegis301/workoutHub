import msgpack
import pandas as pd


def convert_response_data_to_df(response_data):
    response_json = msgpack.unpackb(response_data.content, raw=False)
    return pd.DataFrame(response_json)
