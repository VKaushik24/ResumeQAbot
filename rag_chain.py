from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain.chains import create_history_aware_retriever,create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.messages import HumanMessage,AIMessage
from langchain_groq import ChatGroq

def get_llm ():
    """Initialise Llama 3.1 LLM"""
    llm = ChatGroq(
        model="llama-3.1-70b-versatile",
        temperature=1,
        max_tokens=1024,
        model_kwargs = {"top_p":1},
        stop=None,
    )
    return llm

def get_retreiver_chain(vector_store):
    """Create a retrieval chain to get the similar documents for the query"""
    llm = get_llm()
    retriever = vector_store.as_retriever(search_kwargs={"k":5})
    prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        ("user","{input}"),
        ("user","Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
    ])
    history_retriver_chain = create_history_aware_retriever(llm,retriever,prompt)
    return history_retriver_chain

def get_conversational_rag(history_retriever_chain):
    """Create a history aware retrieval chain """
    llm = get_llm()
    answer_prompt = ChatPromptTemplate.from_messages([
        ("system","Answer the user's questions based on the below context:\n\n{context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user","{input}")
    ])
    document_chain = create_stuff_documents_chain(llm,answer_prompt)
    conversational_retrieval_chain = create_retrieval_chain(history_retriever_chain,document_chain)
    return conversational_retrieval_chain    