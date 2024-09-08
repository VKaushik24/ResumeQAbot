import os
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from Utils.document_loader import load_document,load_url
from Utils.vector_store import get_vector_store
from Utils.rag_chain import get_llm,get_retreiver_chain,get_conversational_rag

# Define the directory to save uploaded files
UPLOAD_DIR = "uploads"

def initialize_session_state():
    """Initialize session state variables."""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history=[
            AIMessage(content="I am a resume bot, how can I help you?")
        ]
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None

def handle_file_upload(uploaded_file, url):
    """Load content from uploaded file or URL and set up the vector store."""
    if uploaded_file or url:
        # Ensure the 'uploads/' directory exists, if not, create it
        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR)
        documents = None
        if url:
            documents = load_url(url)
        elif uploaded_file:
            file_path = f"uploads/{uploaded_file.name}"
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            documents = load_document(file_path)

        if documents:
            st.session_state.vector_store = get_vector_store(documents)
            st.session_state.rag_chain = get_conversational_rag(get_retreiver_chain(st.session_state.vector_store))

def display_chat_history():
    """Display chat history."""
    for message in st.session_state.chat_history:
        message_type = "AI" if isinstance(message, AIMessage) else "Human"
        with st.chat_message(message_type):
            st.markdown(message.content)

def get_response(user_input):
    """Generate a response using the RAG chain."""
    rag_chain = st.session_state.get("rag_chain")
    if not rag_chain:
        st.error("RAG Chain is not initialized.")
        return None
    
    response = rag_chain.invoke({
            "chat_history":st.session_state.chat_history,
            "input":user_input
        })
    return response.get("answer", "No answer found.")

def process_user_input():
    """Handle user input and generate responses."""
    if user_input := st.chat_input("Please ask your question..."):
        st.session_state.chat_history.append(HumanMessage(content=user_input))
        with st.chat_message("Human"):
            st.markdown(user_input)

        response = get_response(user_input)
        if response:
            st.session_state.chat_history.append(AIMessage(content=response))
            with st.chat_message("AI"):
                st.markdown(response)



        
        