import streamlit as st
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_community.embeddings import HuggingFaceEmbeddings
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import qdrant_client.http.models as models
import re


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
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

template = """
Use the provided context to answer the question.

Context:
{context}

Question:
{question}

Answer:
"""

prompt_template = ChatPromptTemplate.from_template(template)
def extract_section_numbers(query):
    return [int(n) for n in re.findall(r"\b(\d+)\b", query)]
section_nums = extract_section_numbers(user_input)
search_results = client.scroll(
    collection_name="bns_sections",
    scroll_filter=models.Filter(
        must=[
            models.FieldCondition(
                key="metadata.sections",
                match=models.MatchAny(section_nums)            )
        ]
    ),
    limit=10,
)