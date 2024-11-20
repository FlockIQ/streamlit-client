import streamlit as st
import src.pages.list_forms as list_forms
import src.pages.create_form as create_form
import src.pages.my_forms as my_forms
import src.pages.fill_form as fill_form
import src.pages.my_responses as my_responses
import src.pages.form_dashboard as form_dashboard
import src.pages.form_analytics as form_analytics

def main():
    st.set_page_config(page_title="Form Builder", layout="wide")

    st.sidebar.title("Form Builder")
    
    # Page selection
    page = st.sidebar.radio(
        "Navigate", 
        [
            "Published Forms",
            "Create Form",
            "My Forms",
            "Fill Form",
            "My Responses",
            "Form Dashboard",
            "Form Analytics"
        ]
    )
    
    # Render selected page
    if page == "Published Forms":
        list_forms.render_page()
    elif page == "Create Form":
        create_form.render_page()
    elif page == "My Forms":
        my_forms.render_page()
    elif page == "Fill Form":
        fill_form.render_page()
    elif page == "My Responses":
        my_responses.render_page()
    elif page == "Form Dashboard":
        form_dashboard.render_page()
    elif page == "Form Analytics":
        form_analytics.render_page()
    else:
        st.error("Page not found.")

if __name__ == "__main__":
    main()
