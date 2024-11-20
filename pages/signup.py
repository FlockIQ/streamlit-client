import streamlit as st
from src.services.auth_service import AuthService

def render_page():
    st.header("Sign Up for FlockIQ")
   
    # Initialize auth service
    auth_service = AuthService()
   
    # Signup form
    with st.form("signup_form"):
        # Basic auth fields
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
       
        # Additional profile fields
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        phone = st.text_input("Phone Number")
       
        # Optional additional fields you might want
        organization = st.text_input("Organization (Optional)")
        bio = st.text_area("Bio (Optional)")
       
        submitted = st.form_submit_button("Sign Up")
       
        if submitted:
            # Validate inputs
            if not email or not password:
                st.error("Email and password are required")
                return
           
            if password != confirm_password:
                st.error("Passwords do not match")
                return
           
            # Prepare profile data for user_info table
            profile_data = {
                'first_name': first_name,
                'last_name': last_name,
                'phone': phone,
                'organization': organization,
                'bio': bio
            }
           
            # Attempt signup
            try:
                user = auth_service.sign_up(email, password, profile_data)
               
                if user:
                    st.success("Account created successfully!")
                    st.info("Please proceed to login.")
                    
                    # Add a button to go to login page
                    if st.button("Go to Login"):
                        st.switch_page("pages/login.py")
                else:
                    st.error("Signup failed")
            except Exception as e:
                st.error(f"Signup error: {str(e)}")
   
    # Add a login link
    st.markdown("Already have an account? ")
    login_col1, login_col2 = st.columns([1, 5])
    with login_col1:
        if st.button("Log In"):
            st.switch_page("pages/login.py")

# This allows the page to be imported and used in the main app
if __name__ == "__main__":
    render_page()