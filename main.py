import streamlit as st
import os
from chatbot import initialize_session_state,handle_file_upload,display_chat_history,process_user_input,get_response
from config import set_api_key


## Set API key for Llama model
set_api_key()

st.set_page_config(page_title="Resume QA Chatbot", page_icon="🤖", layout="centered")
st.title("📝 Resume QA Chatbot powered with Llama 3.1 🦙")

# Initialize session state
initialize_session_state()

# File upload and URL input
uploaded_file = st.file_uploader("Upload your file (.pdf,.docx,.txt)")
url = st.text_input("Or enter the URL of your Resume Site")
load_content = st.button("Upload")

# Handle document load and vector store setup
if st.session_state.vector_store is None:
    handle_file_upload(uploaded_file, url)

# Display chat history
display_chat_history()

# Handle user input and generate responses
process_user_input()

