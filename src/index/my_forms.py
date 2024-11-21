import streamlit as st
import uuid
from datetime import datetime
from src.config.supabase_client import get_supabase_client, get_session, is_user_authenticated
from src.services.form_service import FormService

class MyFormsPage:
    def __init__(self):
        # Ensure user is authenticated
        if not is_user_authenticated():
            st.warning("Please log in to view your forms")
            if st.button("Go to Login", key="login_redirect"):
                st.session_state.active_page = "Login"
            st.stop()

        self.supabase = get_supabase_client()
        self.form_service = FormService(self.supabase)
        self.session = get_session()

    def format_datetime(self, timestamp_str):
        """
        Format timestamp string into readable date and time
        """
        if not timestamp_str:
            return "Date not available", "Time not available"
        
        try:
            # Parse the ISO timestamp
            created_at = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            
            # Convert to local timezone
            local_tz = datetime.now().astimezone().tzinfo
            local_datetime = created_at.astimezone(local_tz)
            
            # Format date and time
            formatted_date = local_datetime.strftime("%B %d, %Y")  # e.g., "November 21, 2024"
            formatted_time = local_datetime.strftime("%I:%M %p")   # e.g., "03:45 PM"
            
            return formatted_date, formatted_time
        except Exception as e:
            print(f"Error formatting datetime: {e}")
            return "Date not available", "Time not available"

    def get_user_forms(self):
        """
        Retrieve forms created by the current user
        """
        try:
            response = (
                self.supabase.table('forms')
                .select('id, created_at, is_public, allow_anon')
                .eq('creator_id', self.session.user.id)
                .execute()
            )
            
            forms = response.data or []
            
            # Add formatted date and time to each form
            for form in forms:
                form['formatted_date'], form['formatted_time'] = self.format_datetime(form.get('created_at'))
            
            return forms
        except Exception as e:
            st.error(f"Error fetching forms: {e}")
            return []

    def get_form_questions(self, form_id):
        """
        Retrieve questions for a specific form
        """
        try:
            response = (
                self.supabase.table('questions')
                .select('*')
                .eq('form_id', form_id)
                .execute()
            )
            return response.data or []
        except Exception as e:
            st.error(f"Error fetching form questions: {e}")
            return []

    def render_form_details_modal(self, form):
        """
        Render a modal with detailed form information
        """
        st.subheader("Form Details")
        
        # Fetch questions for this form
        questions = self.get_form_questions(form['id'])
        
        # Display form metadata with formatted date and time
        st.write(f"**Form ID:** `{form['id']}`")
        st.write(f"**Created on:** {form['formatted_date']} at {form['formatted_time']}")
        st.write(f"**Public Form:** {'Yes' if form['is_public'] else 'No'}")
        st.write(f"**Allows Anonymous Responses:** {'Yes' if form['allow_anon'] else 'No'}")
        
        # Display questions
        st.subheader("Questions")
        for idx, question in enumerate(questions, 1):
            with st.expander(f"Question {idx}"):
                st.write(f"**Text:** {question['questions_text']}")
                st.write(f"**Type:** {question['question_type']}")
                st.write(f"**Required:** {'Yes' if question['is_required'] else 'No'}")
                if question['options']:
                    st.write(f"**Options:** {', '.join(question['options'])}")

    def render_page(self):
        """
        Main page rendering method
        """
        st.title("My Forms")
        
        # Fetch user's forms
        user_forms = self.get_user_forms()
        
        # Display forms in a grid or list
        if not user_forms:
            st.info("You haven't created any forms yet. Click 'Create Form' to get started!")
        else:
            for form in user_forms:
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"Created on: {form['formatted_date']}")
                        st.write(f"Time: {form['formatted_time']}")
                        st.write(f"Public: {'Yes' if form['is_public'] else 'No'}")
                    
                    with col2:
                        if st.button("View Details", key=f"details_{form['id']}"):
                            self.render_form_details_modal(form)
        
        # Create Form button
        st.markdown("---")
        if st.button("Create New Form", use_container_width=True):
            st.session_state.active_page = "Create Form"            

def render_page():
    """
    Entry point for Streamlit page rendering
    """
    page = MyFormsPage()
    page.render_page()

# This allows the page to be imported and used in the main app
if __name__ == "__main__":
    render_page()