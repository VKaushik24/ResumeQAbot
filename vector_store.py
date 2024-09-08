from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_text_splitters.character import CharacterTextSplitter

def get_vector_store(documents):
    """Set up FAISS vector store using HuggingFace embeddings."""
    model_name = "BAAI/bge-large-en-v1.5"
    embeddings = HuggingFaceBgeEmbeddings(
        model_name = model_name,
        model_kwargs = {"device":"cpu"},
        encode_kwargs={'normalize_embeddings': True}
    )

    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000, 
        chunk_overlap=200
    )
    doc_chunks = text_splitter.split_documents(documents)
    
    vector_store = FAISS.from_documents(doc_chunks,embedding = embeddings)
    return vector_store