import streamlit as st
from src.services.auth_service import AuthService

# Import page modules
import pages.list_forms as list_forms
import pages.create_form as create_form
import pages.profile as profile
import pages.welcome as welcome
import pages.home as Home 

def main():
    # Set page configuration to remove padding
    st.set_page_config(page_title="FlockIQ", layout="wide", initial_sidebar_state="collapsed")
   
    # Initialize authentication service
    auth_service = AuthService()
   
    # Global logout function
    def logout():
        auth_service.sign_out()
        st.session_state['logged_in'] = False
        st.switch_page("pages/login.py")
    
    # Check if the user is logged in
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False  # Default to not logged in
    
    # Global logout button
    if st.session_state['logged_in']:
        # Add logout button to the top right of every page
        col1, col2 = st.columns([9, 1])
        with col2:
            if st.button("Logout"):
                logout()
   
    # Render the appropriate page
    if not st.session_state['logged_in']:
        Home.render_page()
    else:
        # Determine the page to render
        desired_page = st.session_state.get('current_page', 'Welcome')
       
        # Create a sidebar for navigation
        st.sidebar.title("FlockIQ")
        st.sidebar.write(f"Welcome, {st.session_state.get('user_email', 'User')}")  # Use session email if available
       
        # Page selection
        page = st.sidebar.radio("Navigate", [
            "Welcome",
            "Published Forms",
            "Create Form",
            "My Forms",
            "Profile"
        ], index=[
            "Welcome", 
            "Published Forms", 
            "Create Form", 
            "My Forms", 
            "Profile"
        ].index(desired_page))
       
        # Clear the current_page from session state after using it
        if 'current_page' in st.session_state:
            del st.session_state['current_page']
       
        # Render selected page
        if page == "Welcome":
            welcome.render_page()
        elif page == "Published Forms":
            list_forms.render_page()
        elif page == "Create Form":
            create_form.render_page()
        elif page == "My Forms":
            list_forms.render_page()
        elif page == "Profile":
            profile.render_page()

if __name__ == "__main__":
    main()
