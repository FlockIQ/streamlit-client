import streamlit as st

def render_page():
    st.title("Welcome to FlockIQ")
   
    st.markdown("""
    ## Platform Overview
   
    FlockIQ is designed to help you create, manage, and distribute forms efficiently.
   
    ### Platform Features
    """)
   
    # Create columns for feature cards
    col1, col2, col3 = st.columns(3)
   
    with col1:
        st.header("Published Forms")
        st.write("Browse and interact with forms shared by others or your organization.")
        if st.button("View Published Forms"):
            st.switch_page("pages/list_forms.py")
   
    with col2:
        st.header("Create Form")
        st.write("Design custom forms tailored to your specific needs.")
        if st.button("Create New Form"):
            st.switch_page("pages/create_form.py")
   
    with col3:
        st.header("My Forms")
        st.write("Manage forms you've created, track responses, and analyze data.")
        if st.button("My Forms"):
            st.switch_page("pages/list_forms.py")
   
    # Additional guidance
    st.markdown("""
    ---
   
    ### Getting Started
    - Use "Published Forms" to find and fill out forms
    - Click "Create Form" to design your own surveys or questionnaires
    - Manage your created forms in "My Forms"
   
    Need help? Check out our profile page for support and account settings.
    """)

# This allows the page to be imported and used in the main app
if __name__ == "__main__":
    render_page()