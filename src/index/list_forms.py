import streamlit as st
from src.config.supabase_client import get_supabase_client
from src.services.form_service import FormService

class ListFormsPage:
    def __init__(self):
        self.supabase = get_supabase_client()
        self.form_service = FormService(self.supabase)

    def get_published_forms(self):
        """
        Retrieve all published forms with additional details
        """
        try:
            response = (
                self.supabase.table('forms')
                .select('id, created_at, creator_id')
                .eq('is_public', True)
                .execute()
            )
            
            # Fetch creator information for each form
            forms = response.data or []
            for form in forms:
                # Get creator's name or email
                user_response = (
                    self.supabase.table('user_info')
                    .select('first_name, last_name, email')
                    .eq('id', form['creator_id'])
                    .execute()
                )
                
                if user_response.data:
                    user = user_response.data[0]
                    form['creator_name'] = (
                        f"{user.get('first_name', '')} {user.get('last_name', '')}".strip() 
                        or user.get('email', 'Unknown Creator')
                    )
                else:
                    form['creator_name'] = 'Unknown Creator'
            
            return forms
        except Exception as e:
            st.error(f"Error fetching published forms: {e}")
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
        
        # Display form metadata
        st.write(f"**Form ID:** `{form['id']}`")
        st.write(f"**Created By:** {form['creator_name']}")
        st.write(f"**Created At:** {form['created_at']}")
        
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
        st.title("Published Forms")
        
        # Search bar (non-functional for now)
        search_term = st.text_input("Search Forms", placeholder="Coming soon...")
        st.info("Search functionality coming soon!")
        
        # Fetch published forms
        published_forms = self.get_published_forms()
        
        # Display forms in a grid or list
        if not published_forms:
            st.info("No published forms available.")
        else:
            for form in published_forms:
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"Created by: {form['creator_name']}")
                        st.write(f"Created on: {form['created_at']}")
                    
                    with col2:
                        if st.button("View Details", key=f"details_{form['id']}"):
                            self.render_form_details_modal(form)

def render_page():
    """
    Entry point for Streamlit page rendering
    """
    page = ListFormsPage()
    page.render_page()

# This allows the page to be imported and used in the main app
if __name__ == "__main__":
    render_page()