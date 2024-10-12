import requests, os

import streamlit as st


def main():
    st.set_page_config(page_title="Hello World")

    st.write("# Welcome to Streamlit!")

    response: requests.Response = requests.get(os.environ["API_URL"] + "/hello", params=dict(user="User"))

    message: str = f"API Server response: {response.json()}." if response.ok else "API Server is offline."

    st.markdown(message)

if __name__ == "__main__":
    main()
