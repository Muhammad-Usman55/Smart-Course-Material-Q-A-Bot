"""
Smart Course Material Q&A Bot with Personality Adaptation
A simple NLP project using LangChain and Streamlit
"""

import streamlit as st
import os
from dotenv import load_dotenv
import tempfile
from bot_core import load_documents, create_vector_store, create_rag_chain, get_answer
from personalities import PERSONALITIES

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Smart Course Q&A Bot",
    page_icon="🤖",
    layout="wide"
)

# --- STATE MANAGEMENT ---
if 'vector_store' not in st.session_state:
    st.session_state.vector_store = None
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'selected_personality' not in st.session_state:
    st.session_state.selected_personality = "Friendly Tutor"

# --- SIDEBAR ---
with st.sidebar:
    st.header("🛠️ Setup")
    
    # File Uploader
    uploaded_file = st.file_uploader(
        "Upload Course Material", 
        type=["pdf", "docx", "txt"],
        help="Upload a PDF, DOCX, or TXT file to get started."
    )

    if uploaded_file:
        if st.button("Process Document"):
            if not os.getenv("GOOGLE_API_KEY"):
                st.error("Please set your GOOGLE_API_KEY in the .env file!")
            else:
                with st.spinner("Processing document..."):
                    # Save the uploaded file temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                        tmp_file.write(uploaded_file.getbuffer())
                        tmp_file_path = tmp_file.name

                    documents = load_documents(tmp_file_path)
                    if documents:
                        st.session_state.vector_store = create_vector_store(documents)
                        st.success("Document processed successfully!")
                        st.session_state.messages = [] # Clear previous messages
                    else:
                        st.error("Unsupported file type or error loading the document.")
                    
                    # Clean up the temporary file
                    os.remove(tmp_file_path)

    st.markdown("---")
    st.header("🎭 Choose a Personality")

    # Personality Selector
    personality_name = st.selectbox(
        "Select a personality for the bot:",
        list(PERSONALITIES.keys()),
        index=list(PERSONALITIES.keys()).index(st.session_state.selected_personality)
    )
    
    if personality_name != st.session_state.selected_personality:
        st.session_state.selected_personality = personality_name
        st.session_state.messages = [] # Clear chat on personality change

    # Display personality info
    st.info(f"{PERSONALITIES[personality_name]['emoji']} {PERSONALITIES[personality_name]['system_message']}")

# --- MAIN CHAT INTERFACE ---
st.title("💬 Smart Course Q&A Bot")
st.caption("Your intelligent assistant for course materials")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask a question about your document..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if st.session_state.vector_store is None:
        st.warning("Please upload and process a document first.")
    else:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                system_message = PERSONALITIES[st.session_state.selected_personality]['system_message']
                
                # Create a new chain for each request to use the updated personality
                rag_chain = create_rag_chain(system_message)
                
                answer, sources = get_answer(st.session_state.vector_store, rag_chain, prompt)
                
                response_content = answer
                st.markdown(response_content)
                
                with st.expander("View Sources"):
                    for i, source in enumerate(sources):
                        st.write(f"**Source {i+1} (Page {source.metadata.get('page', 'N/A')}):**")
                        st.write(source.page_content)
            
            st.session_state.messages.append({"role": "assistant", "content": response_content})
