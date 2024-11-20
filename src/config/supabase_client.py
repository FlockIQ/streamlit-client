import os
from dotenv import load_dotenv
from supabase import create_client, Client
import streamlit as st

# Load environment variables
load_dotenv()

# Initialize Supabase client
url: str = os.getenv("PUBLIC_SUPABASE_URL")
key: str = os.getenv("PUBLIC_SUPABASE_ANON_KEY")

def get_supabase_client() -> Client:
    """
    Creates and returns a Supabase client instance
    """
    try:
        supabase: Client = create_client(url, key)
        return supabase
    except Exception as e:
        print(f"Error initializing Supabase client: {e}")
        raise

def get_session():
    """
    Get the current Supabase session
    """
    supabase = get_supabase_client()
    try:
        session = supabase.auth.get_session()
        return session
    except Exception as e:
        print(f"Error getting session: {e}")
        return None