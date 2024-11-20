import streamlit as st
import sys
import os
from src.config.supabase_client import get_session
from src.services.auth_service import AuthService

# Import page modules
import pages.list_forms as list_forms
import pages.create_form as create_form
import pages.login as login
import pages.signup as signup
import pages.profile as profile
import home  # Import the new home page

def main():
    # Set page configuration to remove padding
    st.set_page_config(page_title="FlockIQ", layout="wide", initial_sidebar_state="collapsed")
    
    # Check authentication status
    session = get_session()
    auth_service = AuthService()
    
    # If not logged in, show home page
    if not session:
        home.render_page()
    else:
        # Logged in user flow
        # Create a sidebar for navigation
        st.sidebar.title("FlockIQ")
        st.sidebar.write(f"Welcome, {session.user.email}")
        
        # Page selection
        page = st.sidebar.radio("Navigate", [
            "Home",
            "Published Forms",
            "Create Form",
            "My Forms",
            "Profile",
            "Logout"
        ])
        
        # Render selected page
        if page == "Home":
            Home.render_page()
        elif page == "Published Forms":
            list_forms.render_page()
        elif page == "Create Form":
            create_form.render_page()
        elif page == "Profile":
            profile.render_page()
        elif page == "Logout":
            # Logout logic
            auth_service.sign_out()
            st.experimental_rerun()

if __name__ == "__main__":
    main()