import streamlit as st
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_community.embeddings import HuggingFaceEmbeddings
import os
from dotenv import load_dotenv

st.set_page_config(page_title="Legal Assistant", page_icon="⚖️", layout="wide")

st.title("Legal Assistant")
st.subheader("Ask questions about BNS sections")

st.write("""
This application helps you find information about BNS sections.
""")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

user_input = st.chat_input("Ask your legal question here...")

if user_input:
    st.chat_message("user").write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    load_dotenv()

    url = os.getenv("QDRANT_CLOUD_URL")
    api_key = os.getenv("QDRANT_API_KEY")

    dense_embedding = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    client = QdrantClient(url=url, api_key=api_key)

    qdrant = QdrantVectorStore(
        client=client,
        collection_name="bns_sections",
        embedding=dense_embedding,
        vector_name="dense",
    )