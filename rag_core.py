import pdfplumber
import pytesseract
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
import os
import google.generativeai as genai
from dotenv import load_dotenv
import re
import unicodedata

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

import re
import unicodedata

def clean_text(text):
    # Remove common headers/footers (customize as needed)
    text = re.sub(r'^.*(HSC.*Bangla.*Paper).*\n?', '', text, flags=re.MULTILINE | re.IGNORECASE)
    # Normalize unicode (for Bangla/English)
    text = unicodedata.normalize("NFKC", text)
    # Remove multiple consecutive newlines
    text = re.sub(r'\n+', '\n', text)
    # Remove excessive spaces
    text = re.sub(r'[ \t]+', ' ', text)
    # Strip leading/trailing whitespace
    text = text.strip()
    return text

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        with pdfplumber.open(pdf) as pdf_reader:
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if not page_text:
                    try:
                        img = page.to_image(resolution=300).original
                        page_text = pytesseract.image_to_string(img, lang='ben+eng')
                    except Exception:
                        page_text = ""
                if page_text:
                    cleaned= clean_text(page_text)

                    text += cleaned+ "\n"
    return text

def get_text_chunks(text, chunk_size=1024, chunk_overlap=300):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.split_text(text)

def get_vector_store(text_chunks, persist_path="faiss_index"):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local(persist_path)

def get_conversational_chain():
    prompt_template = """
    You will be given a pdf as context. Once you get the question look for answer in the whole pdf. Try to reason with it.
    You may even need to calculate or solve a problem based on the context, even need to get the idea.
    Even if you can't find any direct answer, try to answer the question based on the whole pdf.
    Try to be specific in your answer. You may even need to find relation between people on the story 
    or the context in the pdf.
    If you can't find any direct answer try to answer the question based on the whole pdf.
    Don't over justify your answer. Try to be concise.   give the main answer in bold first, then explain a bit if necessary.
    Respond in the same language as the question.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.4)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

def retrieve_and_answer(user_question, persist_path="faiss_index"):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local(persist_path, embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)
    chain = get_conversational_chain()
    response = chain(
        {"input_documents": docs, "question": user_question},
        return_only_outputs=True
    )
    # Return answer and context for evaluation
    context = "\n".join([doc.page_content for doc in docs])
    return response["output_text"], context