from src.config.supabase_client import get_supabase_client

class FormService:
    def __init__(self):
        self.supabase = get_supabase_client()
    
    def get_published_forms(self):
        """
        Retrieve all published forms
        """
        try:
            response = self.supabase.table('forms').select('*').eq('is_public', True).execute()
            return response.data
        except Exception as e:
            print(f"Error fetching published forms: {e}")
            return []
    
    def create_form(self, form_data):
        """
        Create a new form
        """
        try:
            response = self.supabase.table('forms').insert(form_data).execute()
            return response.data
        except Exception as e:
            print(f"Error creating form: {e}")
            return None