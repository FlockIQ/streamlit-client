import streamlit as st
from supabase import create_client, Client

def get_supabase_client() -> Client:
    """
    Creates and returns a Supabase client instance using Streamlit secrets
    """
    try:
        # Retrieve Supabase URL and key from Streamlit secrets
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        
        supabase: Client = create_client(url, key)
        return supabase
    except Exception as e:
        st.error(f"Error initializing Supabase client: {e}")
        raise

def get_session():
    """
    Get the current Supabase session
    """
    try:
        supabase = get_supabase_client()
        session = supabase.auth.get_session()
        return session
    except Exception as e:
        st.error(f"Error getting session: {e}")
        return None