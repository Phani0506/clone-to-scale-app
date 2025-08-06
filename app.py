# FILE: app.py
# ACTION: Replace the entire content of your existing app.py with this.

import streamlit as st
import yaml
import os
import sys
from dotenv import load_dotenv

# --- Page Configuration (MUST BE THE FIRST STREAMLIT COMMAND) ---
st.set_page_config(
    page_title="Clone to Scale - AI Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)

# --- Add project root to Python path ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
# ---

from src.data_ingestion import load_from_directory, load_from_urls
from src.indexing import build_index
from src.query_engine import create_query_engine_from_index

# --- Load Environment Variables ---
load_dotenv()

# --- App Title ---
st.title("Clone to Scale - AI Assistant 🤖")
st.caption("A multi-domain RAG-powered AI assistant.")

# --- Domain Selection ---
st.sidebar.header("Configuration")
domain_options = {
    "AI Education": "ai_education",
    "Higher Education Counselling": "higher_ed_counselling",
    "Medical Pediatrics": "medical_pediatrics",
}

selected_domain_name = st.sidebar.selectbox(
    "Choose your AI Assistant:",
    options=list(domain_options.keys())
)
selected_domain_key = domain_options[selected_domain_name]

# --- Caching the Query Engine ---
@st.cache_resource(show_spinner="Building AI Assistant... This may take a few minutes.")
def load_and_build_index(domain):
    """Loads data, builds the index in memory, and returns the index object."""
    try:
        config_path = f"configs/{domain}_config.yaml"
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        local_docs = load_from_directory(config['local_data_path'])
        web_docs = load_from_urls(config['urls_to_scrape'])
        all_documents = local_docs + web_docs

        if not all_documents:
            st.error(f"No documents found for domain '{domain}'. Cannot build index.")
            return None, None

        index = build_index(
            config['vector_collection_name'],
            all_documents
        )
        return index, config.get('system_prompt')

    except Exception as e:
        st.error(f"Failed to build the AI assistant for '{domain}'.")
        st.error(f"Error: {e}")
        return None, None

# Load the index and prompt for the selected domain
index_and_prompt = load_and_build_index(selected_domain_key)
if index_and_prompt and index_and_prompt[0] is not None:
    index, system_prompt = index_and_prompt
    query_engine = create_query_engine_from_index(index, system_prompt)
else:
    query_engine = None


# --- Chat Interface ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_domain" not in st.session_state or st.session_state.current_domain != selected_domain_key:
    st.session_state.messages = []
    st.session_state.current_domain = selected_domain_key
    st.info(f"Switched to {selected_domain_name} assistant. Start a new conversation!")


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask your question..."):
    if query_engine:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = query_engine.query(prompt)
                response_text = str(response)
                st.markdown(response_text)
        
        st.session_state.messages.append({"role": "assistant", "content": response_text})
    else:
        st.warning("The AI Assistant is not available. Please check the configuration.")
