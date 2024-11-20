import streamlit as st
import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Initialize Supabase credentials
url: str = os.getenv("PUBLIC_SUPABASE_URL")
key: str = os.getenv("PUBLIC_SUPABASE_ANON_KEY")

def get_supabase_client() -> Client:
    """
    Creates and returns a Supabase client instance.
    """
    try:
        supabase: Client = create_client(url, key)
        return supabase
    except Exception as e:
        st.error(f"Error initializing Supabase client: {e}")
        raise

# Streamlit UI
st.title("Supabase Configuration")

# Display the Supabase URL
if url:
    st.subheader("Supabase URL")
    st.write(url)
else:
    st.error("SUPABASE_URL is not set in the environment variables.")
