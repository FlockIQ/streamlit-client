from src.config.supabase_client import get_supabase_client
import streamlit as st

class AuthService:
    def __init__(self):
        self.supabase = get_supabase_client()
   
    def sign_up(self, email, password, profile_data):
        """
        Sign up a new user
        """
        try:
            # Prepare signup data
            signup_data = {
                "email": email,
                "password": password
            }
           
            # Create user in Supabase Auth
            response = self.supabase.auth.sign_up(signup_data)
           
            # If signup is successful, add additional profile data
            if response.user:
                user_id = response.user.id
                # Insert additional profile data into user_info table
                profile_data['id'] = user_id
                self.update_profile(user_id, profile_data)
               
                return response.user
           
            return None
        except Exception as e:
            # More detailed error handling
            st.error(f"Signup error: {str(e)}")
            raise

    def sign_in(self, email, password):
        """
        Sign in a user with more robust error handling
        """
        try:
            # Attempt to sign in with email and password
            response = self.supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
        
            # Check if user is successfully authenticated
            if response and response.user:
                # Set session state for logged-in user
                st.session_state['logged_in'] = True
                st.session_state['current_page'] = 'Welcome'
                return response.user  # User is authenticated
            else:
                raise ValueError("Authentication failed")
        
        except Exception as e:
            print(f"Login error details: {str(e)}")
            raise ValueError("Invalid email or password")

    
    def sign_out(self):
        """
        Sign out the current user
        """
        try:
            self.supabase.auth.sign_out()
            return True
        except Exception as e:
            st.error(f"Logout error: {str(e)}")
            return False
    
    def get_user_profile(self, user_id):
        """
        Retrieve user profile data
        """
        try:
            # Use user_info table instead of users
            response = self.supabase.table('user_info').select('*').eq('id', user_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Error fetching profile: {str(e)}")
            return None
    
    def update_profile(self, user_id, profile_data):
        """
        Update user profile
        """
        try:
            # Remove None or empty values
            profile_data = {k: v for k, v in profile_data.items() if v}
            
            # Upsert (insert or update) profile data in user_info table
            response = self.supabase.table('user_info').upsert({
                'id': user_id,
                **profile_data
            }).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Error updating profile: {str(e)}")
            return None