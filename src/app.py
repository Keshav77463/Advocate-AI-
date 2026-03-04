import streamlit as st

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