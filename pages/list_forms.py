import streamlit as st
from src.services.form_service import FormService

def render_page():
    st.title("Published Forms")
    
    # Initialize form service
    form_service = FormService()
    
    # Fetch published forms
    published_forms = form_service.get_published_forms()
    
    # Display forms
    if published_forms:
        for form in published_forms:
            st.write(f"Form: {form['id']}")
            # Add more details and interaction
    else:
        st.write("No published forms available")

# This allows the page to be imported and used in the main app
if __name__ == "__main__":
    render_page()