import streamlit as st
from src.services.form_service import FormService

def render_page():
    st.title("Create Form")


# This allows the page to be imported and used in the main app
if __name__ == "__main__":
    render_page()