import streamlit as st

def check_login(username, password):
    return (
        username == st.secrets["USERNAME"]
        and password == st.secrets["PASSWORD"]
    )
