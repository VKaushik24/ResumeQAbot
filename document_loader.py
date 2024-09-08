import os
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.document_loaders import TextLoader, WebBaseLoader,Docx2txtLoader
import streamlit as st
def load_document(file_path):
    """Load documents from a file based on its type."""
    file_extension = os.path.splitext(file_path)[1]
    if file_extension == '.pdf':
        loader = PyPDFLoader(file_path)
    elif file_extension == '.docx':
        loader = Docx2txtLoader(file_path)
    elif file_extension == '.txt':
        loader = TextLoader(file_path)
    else:
        st.error("Not a valid format")
        return None
    return loader.load()

def load_url(url):
    """Load documents from a web URL."""
    loader = WebBaseLoader(url)
    return loader.load()