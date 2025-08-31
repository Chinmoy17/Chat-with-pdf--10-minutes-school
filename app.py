import streamlit as st
from rag_core import get_pdf_text, get_text_chunks, get_vector_store, retrieve_and_answer, scrape_website, process_urls

# --- Caching Functions ---
@st.cache_data
def cached_get_pdf_text(pdf_files_content):
    return get_pdf_text(pdf_files_content)

@st.cache_data
def cached_scrape_website(url):
    return scrape_website(url)

@st.cache_data
def cached_process_urls(urls):
    return process_urls(urls)

def main():
    st.set_page_config(layout="wide", page_title="PDF-Alap")

    # --- HEADER ---
    st.title("PDF-Alap: Your AI Research Assistant 📄✨")
    st.markdown("Upload research papers, your CV, and professor details to get help with your research and draft compelling emails.")

    # --- MAIN CHAT INTERFACE ---
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])

    user_question = st.chat_input("Ask a question or request an email draft...")

    if user_question:
        st.session_state.chat_history.append({"role": "user", "content": user_question})
        cv_text = st.session_state.get("cv_text", "")
        scraped_text = st.session_state.get("scraped_text", "")
        
        with st.spinner("Thinking..."):
            answer, _ = retrieve_and_answer(user_question, cv_text=cv_text, scraped_text=scraped_text)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            st.rerun()

    # --- SIDEBAR FOR DATA INPUT ---
    with st.sidebar:
        st.header("Data Input")
        
        tab1, tab2 = st.tabs(["Upload Files", "From URL"])

        with tab1:
            st.subheader("Upload Research Papers")
            pdf_docs = st.file_uploader(
                "Upload PDF files of research papers.",
                accept_multiple_files=True, type=["pdf"], key="pdf_uploader"
            )
            
            st.subheader("Upload Your CV")
            cv_file = st.file_uploader(
                "Upload your CV in PDF format.", 
                type=["pdf"], key="cv_uploader"
            )

        with tab2:
            st.subheader("Paper URLs")
            paper_urls = st.text_area("Paste paper URLs (one per line)", key="paper_urls")
            
            st.subheader("Professor's Website")
            prof_url = st.text_input("Paste professor's website or Google Scholar URL", key="prof_url")

        if st.button("Submit & Process"):
            with st.spinner("Processing all inputs..."):
                paper_text_list = []
                
                # Process uploaded PDFs
                if pdf_docs:
                    pdf_content = [file.getvalue() for file in pdf_docs]
                    paper_text_list.append(cached_get_pdf_text(tuple(pdf_content)))
                
                # Process paper URLs
                if paper_urls:
                    urls = tuple(paper_urls.strip().split('\n'))
                    paper_text_list.append(cached_process_urls(urls))

                st.session_state.paper_text = "\n".join(paper_text_list)

                # Process CV
                if cv_file:
                    cv_content = cv_file.getvalue()
                    st.session_state.cv_text = cached_get_pdf_text((cv_content,))
                
                # Process professor's URL
                if prof_url:
                    st.session_state.scraped_text = cached_scrape_website(prof_url)
                
                # Create vector store from combined paper text
                if st.session_state.get("paper_text"):
                    text_chunks = get_text_chunks(st.session_state.paper_text)
                    get_vector_store(text_chunks)
                    st.success("All inputs processed and ready!")
                else:
                    st.warning("Please provide at least one research paper (file or URL).")

if __name__ == "__main__":
    main()