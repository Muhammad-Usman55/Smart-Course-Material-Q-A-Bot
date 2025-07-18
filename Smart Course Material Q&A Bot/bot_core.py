"""
Core Q&A Bot Logic using LangChain
"""

import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate


def load_documents(file_path):
    """Load documents from a file path."""
    _, extension = os.path.splitext(file_path)
    if extension.lower() == '.pdf':
        loader = PyPDFLoader(file_path)
    elif extension.lower() == '.txt':
        loader = TextLoader(file_path)
    elif extension.lower() == '.docx':
        loader = Docx2txtLoader(file_path)
    else:
        return None
    return loader.load()

def create_vector_store(documents):
    """Create a FAISS vector store from documents."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(documents)
    embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=os.environ["GOOGLE_API_KEY"])
    vector_store = FAISS.from_documents(docs, embedding=embedding_model)
    return vector_store

def create_rag_chain(system_message):
    """Create a RAG chain with a custom system message."""
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7, convert_system_message_to_human=True)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("human", "CONTEXT:\n{context}\n\nQUESTION:\n{input}\n\nANSWER:")
    ])

    chain = create_stuff_documents_chain(llm, prompt)
    return chain

def get_answer(vector_store, chain, query):
    """Get an answer from the RAG chain."""
    retriever = vector_store.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, chain)
    
    response = retrieval_chain.invoke({"input": query})
    
    return response['answer'], response['context']
