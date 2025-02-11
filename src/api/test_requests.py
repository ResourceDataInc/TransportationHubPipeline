"""
Fires off a request to the local API, printing predicted values.

- jrgarrar
"""

# SETUP #######################################################################
# Import libraries.
import requests
from datetime import datetime

API_URL = "http://127.0.0.1:5000/api/v1/predict"

# HELPERS #####################################################################
def datetime_to_timestamp(d):
    d_formatted = datetime.strptime(d, '%Y-%m-%d %H:%M:%S')
    d_unix_timestamp = d_formatted.timestamp()
    d_payload = {"TIMESTAMP": d_unix_timestamp}
    return d_payload

def post_and_print(d):
    print(f'Input: {d}')
    r = requests.post(API_URL, json=datetime_to_timestamp(d))
    print(f'Output: {r.text}')


# MAIN ########################################################################
def main():
    # Fire off various requests an print the outputs.
    post_and_print("2023-09-19 18:33:43")
    post_and_print("2023-09-19 19:33:43")
    post_and_print("2023-09-19 20:33:43")

if __name__ == "__main__":
    main()
