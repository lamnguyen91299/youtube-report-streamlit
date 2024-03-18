import streamlit as st
import os

# Check if the app is running in Streamlit Cloud
if "openai_api_key" in st.secrets and "youtube_api_key" in st.secrets:
    # Use Streamlit Secrets if running in Streamlit Cloud
    openai_api_key = st.secrets["openai_api_key"]
    youtube_api_key = st.secrets["youtube_api_key"]
else:
    # Load environment variables if running locally
    from dotenv import load_dotenv
    load_dotenv()
    openai_api_key = os.getenv("openai_api_key")
    youtube_api_key = os.getenv("youtube_api_key")

# Print the API keys (for testing purposes)
print(openai_api_key)
print(youtube_api_key)