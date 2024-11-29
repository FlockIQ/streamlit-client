import streamlit as st
from src.config.supabase_client import get_supabase_client
from src.services.form_service import FormService
from datetime import datetime

class ListFormsPage:
    def __init__(self):
        self.supabase = get_supabase_client()
        self.form_service = FormService(self.supabase)

    def format_datetime(self, timestamp_str):
        if not timestamp_str:
            return "Date not available", "Time not available"
        try:
            created_at = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            local_tz = datetime.now().astimezone().tzinfo
            local_datetime = created_at.astimezone(local_tz)
            return local_datetime.strftime("%B %d, %Y"), local_datetime.strftime("%I:%M %p")
        except Exception as e:
            print(f"Error formatting datetime: {e}")
            return "Date not available", "Time not available"

    def get_published_forms(self):
        try:
            forms_response = (
                self.supabase.table('forms')
                .select('id, created_at, is_public, allow_anon, form_title, form_description, creator_id')
                .eq('is_public', True)
                .execute()
            )
            
            forms = forms_response.data or []
            
            for form in forms:
                if not form.get('creator_id'):
                    form['creator_name'] = 'Unknown Creator'
                    continue

                user_info_response = (
                    self.supabase.table('user_info')
                    .select('first_name, last_name, email')
                    .eq('id', form['creator_id'])
                    .execute()
                )

                if user_info_response.data:
                    user_info = user_info_response.data[0]
                    name_parts = [user_info.get('first_name', ''), user_info.get('last_name', '')]
                    form['creator_name'] = ' '.join(filter(None, name_parts)) or user_info.get('email', 'Unknown Creator')
                else:
                    form['creator_name'] = 'Unknown Creator'
                
                form['formatted_date'], form['formatted_time'] = self.format_datetime(form.get('created_at'))

            return forms
        except Exception as e:
            st.error(f"Error fetching published forms: {str(e)}")
            return []

    def get_form_questions(self, form_id):
        try:
            response = self.supabase.table('questions').select('*').eq('form_id', form_id).execute()
            return response.data or []
        except Exception as e:
            st.error(f"Error fetching form questions: {e}")
            return []

    @st.dialog("Form Details")
    def render_form_details_dialog(self, form):
        st.write(f"**Title:** {form['form_title']}")
        st.write(f"**Description:** {form['form_description']}")
        st.write(f"**Created on:** {form['formatted_date']} at {form['formatted_time']}")
        st.write(f"**Allows Anonymous Responses:** {'Yes' if form['allow_anon'] else 'No'}")
        
        st.subheader("Questions")
        questions = self.get_form_questions(form['id'])
        for idx, question in enumerate(questions, 1):
            with st.expander(f"Question {idx}"):
                st.write(f"**Text:** {question['questions_text']}")
                st.write(f"**Type:** {question['question_type']}")
                st.write(f"**Required:** {'Yes' if question['is_required'] else 'No'}")
                if question['options']:
                    st.write(f"**Options:** {', '.join(question['options'])}")
        
        if st.button("Fill form", key=f"fill_{form['id']}_popup"):
                            self.redirect_to_fill_form(form['id'])

    def redirect_to_fill_form(self, form_id):
        st.session_state.active_page = "Fill Form"
        st.session_state.form_id = form_id
        st.rerun()

    def render_page(self):
        st.title("Published Forms")
        search_term = st.text_input("Search Forms", placeholder="Coming soon...")
        st.info("Search functionality coming soon!")
        
        published_forms = self.get_published_forms()
        
        if not published_forms:
            st.info("No published forms available.")
        else:
            for form in published_forms:
                with st.container(border=True):
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.write(f"**Created by:** {form['creator_name']}")
                        st.write(f"**Title:** {form['form_title']}")
                        st.write(f"**Created on:** {form['formatted_date']} at {form['formatted_time']}")
                    
                    with col2:
                        if st.button("View Details", key=f"details_{form['id']}"):
                            self.render_form_details_dialog(form)
                    
                    with col3:
                        if st.button("Fill Form", key=f"fill_{form['id']}"):
                            self.redirect_to_fill_form(form['id'])

def render_page():
    page = ListFormsPage()
    page.render_page()

if __name__ == "__main__":
    render_page()