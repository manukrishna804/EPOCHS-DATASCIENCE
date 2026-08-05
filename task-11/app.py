import streamlit as st
from rag_pipeline import (
    load_pdf,
    split_documents,
    create_vector_store,
    retrieve_chunks,
    generate_answer,
    ConversationMemory
)

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="PDF QA RAG Assistant",
    page_icon="📄",
    layout="wide"
)

# -----------------------------
# Session State
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "memory" not in st.session_state:
    st.session_state.memory = ConversationMemory()

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

# -----------------------------
# Title
# -----------------------------
st.title("📄 PDF QA RAG Assistant")
st.write("Upload a PDF and ask questions about it.")

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:

    st.header("Settings")

    uploaded_file = st.file_uploader(
        "Upload a PDF",
        type="pdf"
    )

    if uploaded_file:

        # Create vector DB only once
        if st.session_state.vector_store is None:

            documents = load_pdf(uploaded_file)

            chunks = split_documents(documents)

            st.session_state.vector_store = create_vector_store(chunks)

            st.success("✅ Vector database created successfully!")

            st.success(
                f"Loaded {len(documents)} pages and created {len(chunks)} chunks."
            )

            with st.expander("First Chunk Preview"):
                st.write(chunks[0].page_content)

    if st.button("🗑️ Clear Chat"):

        st.session_state.messages = []

        st.session_state.memory.clear()

        st.session_state.vector_store = None

        st.rerun()

# -----------------------------
# Display Previous Messages
# -----------------------------
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        # Display Sources
        if (
            message["role"] == "assistant"
            and "sources" in message
        ):

            with st.expander("📄 View Sources"):

                for i, doc in enumerate(message["sources"], start=1):

                    page = doc.metadata.get("page", 0)

                    st.markdown(f"### Source {i}")
                    st.write(f"**Page:** {page + 1}")
                    st.write(doc.page_content)
                    st.divider()

# -----------------------------
# Chat Input
# -----------------------------
question = st.chat_input("Ask a question about your PDF...")

if question:

    if st.session_state.vector_store is None:

        st.error("Please upload a PDF first.")

        st.stop()

    # Show user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    st.session_state.memory.add_user_message(question)

    with st.chat_message("user"):
        st.markdown(question)

    # Retrieve documents
    results = retrieve_chunks(
        st.session_state.vector_store,
        question
    )

    # Generate answer
    with st.spinner("Thinking..."):

        answer = generate_answer(
            question,
            results,
            st.session_state.memory.get_history()
        )

    st.session_state.memory.add_ai_message(answer)

    # Save assistant response + sources
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": results
        }
    )

    # Display assistant response
    with st.chat_message("assistant"):

        st.markdown(answer)

        with st.expander("📄 View Sources"):

            for i, doc in enumerate(results, start=1):

                page = doc.metadata.get("page", 0)

                st.markdown(f"### Source {i}")
                st.write(f"**Page:** {page + 1}")
                st.write(doc.page_content)
                st.divider()