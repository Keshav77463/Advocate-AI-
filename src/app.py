import streamlit as st
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http import models
import os
import re
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

st.set_page_config(page_title="Legal Assistant", page_icon="⚖️", layout="wide")
st.title("Legal Assistant")
st.subheader("Ask questions about BNS sections")
st.write("""
    This application helps you find information about BNS sections. You can:
    - Ask about specific section numbers (e.g., "What does section 123 say about...")
    - Ask general questions about legal topics
""")

url = os.getenv("QDRANT_CLOUD_URL")
api_key = os.getenv("QDRANT_API_KEY")
collection_name = "bns_sections"

@st.cache_resource
def load_resources():
    dense_embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    client = QdrantClient(url=url, api_key=api_key, timeout=60)
    qdrant = QdrantVectorStore(
        client=client,
        collection_name=collection_name,
        embedding=dense_embedding,
        vector_name="dense",
    )
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        thinking_budget=1024,
        include_thoughts=True
    )
    return client, qdrant, llm

client, qdrant, llm = load_resources()


def extract_section_numbers(query):
    return [int(n) for n in re.findall(r"\b(\d+)\b", query)]


def format_docs(docs):
    formatted_text = ""
    for i, doc in enumerate(docs):
        section_num = doc.metadata.get('sections', 'N/A')
        formatted_text += f"Document {i + 1} (Section {section_num}):\n{doc.page_content}\n\n"
    return formatted_text


def get_clean_response(response):
    """Strip thinking tokens from Gemini response if present."""
    content = response.content
    if isinstance(content, list):
        # Filter out thinking blocks, keep only text
        return " ".join(block.text for block in content if hasattr(block, "text") and block.type == "text")
    # Remove <thinking>...</thinking> tags if returned as string
    return re.sub(r"<thinking>.*?</thinking>", "", content, flags=re.DOTALL).strip()


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

user_input = st.chat_input("Ask your legal question here...")

if user_input:
    st.chat_message("user").write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        with st.spinner("Searching for information..."):
            try:
                section_nums = extract_section_numbers(user_input)

                if section_nums:
                    st.info(f"Found section numbers in your query: {section_nums}")
                    # FIX: Use the raw client for filtered searches (more reliable)
                    search_results = client.scroll(
                        collection_name=collection_name,
                        scroll_filter=models.Filter(
                            must=[
                                models.FieldCondition(
                                    key="metadata.sections",
                                    match=models.MatchAny(any=section_nums)
                                )
                            ]
                        ),
                        limit=10,
                        with_payload=True,
                        with_vectors=False
                    )
                    # Convert scroll results to doc-like objects
                    from types import SimpleNamespace
                    results = [
                        SimpleNamespace(
                            page_content=point.payload.get("page_content", ""),
                            metadata=point.payload.get("metadata", {})
                        )
                        for point in search_results[0]
                    ]
                else:
                    results = qdrant.similarity_search(user_input, k=5)

                if not results:
                    st.warning("No relevant sections found for your query.")
                    st.stop()

                context = format_docs(results)

                template = """
                Use the provided context to answer the question.
                If the answer is not fully contained in the context,
                use your reasoning to provide a helpful explanation
                acting like a legal assistant.

                Context:
                {context}

                Question:
                {question}

                Answer:
                """

                prompt_template = ChatPromptTemplate.from_template(template)
                chain = prompt_template | llm
                response = chain.invoke({"context": context, "question": user_input})

                clean_response = get_clean_response(response)
                st.write(clean_response)
                st.session_state.messages.append({"role": "assistant", "content": clean_response})

                with st.expander("View Source Documents"):
                    st.text(context)

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")