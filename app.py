
import streamlit as st
from rag_core import get_pdf_text, get_text_chunks, get_vector_store, retrieve_and_answer

def main():
    st.set_page_config("Chat PDF")
    st.header("Chat with PDF Locally 💁")

    # Initialize chat history in session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history using chat_message
    for chat in st.session_state.chat_history:
        with st.chat_message("user"):
            st.markdown(chat["question"])
        with st.chat_message("assistant"):
            st.markdown(chat["answer"])

    # Chat input at the bottom
    user_question = st.chat_input("Next Question?")

    if user_question:
        answer, _ = retrieve_and_answer(user_question)
        st.session_state.chat_history.append({"question": user_question, "answer": answer})
        # Rerun to display the new message immediately
        st.rerun()

    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader(
            "Upload your PDF Files and Click on the Submit & Process Button",
            accept_multiple_files=True, type=["pdf"]
        )
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                st.success("Done")

if __name__ == "__main__":
    main()