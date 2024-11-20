import streamlit as st
from src.config.supabase_client import get_session

def render_page():
    # Check if user is not logged in
    session = get_session()
    
    if not session:
        st.title("Welcome to FlockIQ")
        
        st.markdown("""
        ## Revolutionize Your Surveys and Forms
        
        FlockIQ is more than just a form builder. It's your powerful tool for creating, distributing, and analyzing surveys with unprecedented ease and insight.
        
        ### Why FlockIQ?
        
        - 🚀 **Effortless Form Creation**: As simple as Google Forms, but with superpowers
        - 📊 **Enhanced Analytics**: Deep insights beyond basic form responses
        - 🔒 **Secure**: Enterprise-grade security for your data
        
        ### Get Started
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Login", use_container_width=True):
                st.switch_page("pages/login.py")
        
        with col2:
            if st.button("Sign Up", use_container_width=True):
                st.switch_page("pages/signup.py")
        
        # Optional: Add a brief feature showcase or preview
        st.markdown("---")
        st.markdown("#### Quick Preview")
        st.image("media\logo.png", width=200)  # Replace with your logo path
    
    else:
        # If logged in, show a welcome dashboard
        st.title(f"Welcome Back to FlockIQ, {session.user.email}")
        
        # You can add quick actions or recent form previews here
        st.markdown("""
        ### Quick Actions
        - Create a New Form
        - View Published Forms
        - Check Analytics
        """)

# This allows the page to be imported and used in the main app
if __name__ == "__main__":
    render_page()