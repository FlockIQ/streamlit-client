import streamlit as st
import uuid
from typing import List, Dict, Any
from src.config.supabase_client import get_supabase_client, get_session
from src.services.form_service import FormService

class FormCreationPage:
    def __init__(self):
        self.supabase = get_supabase_client()
        self.form_service = FormService(self.supabase)
        self.session = get_session()

    def validate_form(self, form_title: str, questions: List[Dict[str, Any]]) -> bool:
        """
        Validate form before submission
        """
        if not form_title.strip():
            st.error("Form title cannot be empty")
            return False
        
        if not questions:
            st.error("Please add at least one question to the form")
            return False
        
        for idx, question in enumerate(questions, 1):
            if not question.get('text'):
                st.error(f"Question {idx} text cannot be empty")
                return False
            
            if question.get('type') == 'multiple_choice' and not question.get('options'):
                st.error(f"Multiple choice question {idx} must have options")
                return False
        
        return True

    def render_question_input(self, index: int) -> Dict[str, Any]:
        """
        Render individual question input fields
        """
        st.subheader(f"Question {index}")
        
        # Question text
        question_text = st.text_input(
            f"Question {index} Text", 
            key=f"question_text_{index}"
        )
        
        # Question type selection
        question_type = st.selectbox(
            f"Question {index} Type", 
            ['Short Text', 'Paragraph', 'Multiple Choice', 'Checkboxes', 'Dropdown'],
            key=f"question_type_{index}"
        )
        
        # Optional settings
        is_required = st.checkbox(
            "Required Question", 
            key=f"is_required_{index}"
        )
        
        # Additional options based on question type
        options = []
        if question_type == 'Multiple Choice' or question_type == 'Checkboxes' or question_type == 'Dropdown':
            option_input = st.text_input(
                f"Enter options (comma-separated)", 
                key=f"options_{index}"
            )
            options = [opt.strip() for opt in option_input.split(',') if opt.strip()]
        
        return {
            'text': question_text,
            'type': question_type.lower().replace(' ', '_'),
            'is_required': is_required,
            'options': options if options else None,
            'id': str(uuid.uuid4())
        }

    def render_page(self):
        """
        Main page rendering method
        """
        st.title("Create a New Form")
        
        # Ensure user is logged in
        if not self.session:
            st.warning("Please log in to create a form")
            return

        # Form title
        form_title = st.text_input("Form Title")
        form_description = st.text_area("Form Description (Optional)")

        # Form privacy settings
        is_public = st.checkbox("Make form publicly accessible")
        allow_anonymous = st.checkbox("Allow anonymous responses")

        # Dynamic question addition
        st.header("Questions")
        
        # Session state to manage questions dynamically
        if 'questions' not in st.session_state:
            st.session_state.questions = []

        # Add question button
        if st.button("➕ Add Question"):
            st.session_state.questions.append({})

        # Render existing questions
        questions_to_save = []
        for idx, _ in enumerate(st.session_state.questions, 1):
            with st.expander(f"Question {idx}", expanded=True):
                question = self.render_question_input(idx)
                questions_to_save.append(question)

        # Remove question functionality
        if st.session_state.questions and st.button("🗑️ Remove Last Question"):
            st.session_state.questions.pop()
            st.experimental_rerun()

        # Submit form
        if st.button("Create Form"):
            if self.validate_form(form_title, questions_to_save):
                try:
                    # Create form with all details
                    form_data = {
                        'title': form_title,
                        'description': form_description,
                        'is_public': is_public,
                        'allow_anonymous': allow_anonymous
                    }
                    
                    new_form = self.form_service.create_form(
                        creator_id=self.session.user.id,
                        form_data=form_data,
                        questions=questions_to_save
                    )
                    
                    if new_form:
                        st.success("Form created successfully!")
                        # Optional: Reset form or redirect
                        st.session_state.questions = []
                    else:
                        st.error("Failed to create form")
                
                except Exception as e:
                    st.error(f"Error creating form: {e}")

def render_page():
    """
    Entry point for Streamlit page rendering
    """
    page = FormCreationPage()
    page.render_page()

# This allows the page to be imported and used in the main app
if __name__ == "__main__":
    render_page()