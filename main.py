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
import Home  # Import the new home page

def main():
    # Set page configuration to remove padding
    st.set_page_config(page_title="FlockIQ", layout="wide", initial_sidebar_state="collapsed")
    
    # Check authentication status
    session = get_session()
    auth_service = AuthService()
    
    # If not logged in, show home page
    if not session:
        Home.render_page()
    else:
        # Check if there's a desired page from login
        desired_page = st.session_state.get('current_page', 'Home')
        
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
        ], index=["Home", "Published Forms", "Create Form", "My Forms", "Profile", "Logout"].index(desired_page))
        
        # Clear the current_page from session state after using it
        if 'current_page' in st.session_state:
            del st.session_state['current_page']
        
        # Render selected page
        if page == "Home":
            Home.render_page()
        elif page == "Published Forms":
            list_forms.render_page()
        elif page == "Create Form":
            create_form.render_page()
        elif page == "My Forms":
            list_forms.render_page()  # Assuming this is the same as Published Forms
        elif page == "Profile":
            profile.render_page()
        elif page == "Logout":
            # Logout logic
            auth_service.sign_out()
            st.rerun()

if __name__ == "__main__":
    main()