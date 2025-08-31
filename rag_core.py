import pdfplumber
import pytesseract
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
import os
import google.generativeai as genai
from dotenv import load_dotenv
import re
import unicodedata
from config import settings
import requests
from bs4 import BeautifulSoup
import io

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def clean_text(text):
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    text = text.strip()
    return text

def get_pdf_text(pdf_files_content):
    text = ""
    for content in pdf_files_content:
        with pdfplumber.open(io.BytesIO(content)) as pdf_reader:
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if not page_text:
                    try:
                        img = page.to_image(resolution=300).original
                        page_text = pytesseract.image_to_string(img, lang='ben+eng')
                    except Exception:
                        page_text = ""
                if page_text:
                    cleaned = clean_text(page_text)
                    text += cleaned + "\n"
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=settings.CHUNK_SIZE, chunk_overlap=settings.CHUNK_OVERLAP)
    return text_splitter.split_text(text)

def get_vector_store(text_chunks, persist_path="chroma_db"):
    embeddings = GoogleGenerativeAIEmbeddings(model=settings.EMBEDDING_MODEL)
    vector_store = Chroma.from_texts(text_chunks, embedding=embeddings, persist_directory=persist_path)
    vector_store.persist()

def get_examples():
    return ""

def get_conversational_chain():
    with open("config/system_prompt.txt", "r", encoding="utf-8") as f:
        prompt = f.read()
    
    prompt_template = f"""{prompt}

**Provided Context:**

*User's CV details:*
{{cv_text}}

*Professor's website information:*
{{scraped_text}}

*Relevant content from research papers:*
{{context}}

**User's Request:**
{{question}}

**Answer:**
"""
    
    model = ChatGoogleGenerativeAI(model=settings.LLM_MODEL, temperature=settings.TEMPERATURE)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question", "cv_text", "scraped_text"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

def scrape_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        text = ' '.join(soup.stripped_strings)
        return text
    except requests.exceptions.RequestException as e:
        return f"An error occurred while scraping: {e}"

def process_urls(urls):
    text = ""
    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
            if 'application/pdf' in response.headers.get('Content-Type', ' '):
                with pdfplumber.open(io.BytesIO(response.content)) as pdf_reader:
                    for page in pdf_reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += clean_text(page_text) + "\n"
            else:
                soup = BeautifulSoup(response.content, "html.parser")
                text += clean_text(' '.join(soup.stripped_strings)) + "\n"
        except requests.exceptions.RequestException as e:
            print(f"Could not process URL {url}: {e}")
    return text

def retrieve_and_answer(user_question, cv_text="", scraped_text="", persist_path="chroma_db"):
    embeddings = GoogleGenerativeAIEmbeddings(model=settings.EMBEDDING_MODEL)
    vector_store = Chroma(persist_directory=persist_path, embedding_function=embeddings)
    docs = vector_store.similarity_search(user_question)
    
    context = "\n".join([doc.page_content for doc in docs])
    
    chain = get_conversational_chain()
    response = chain(
        {
            "input_documents": docs, 
            "question": user_question,
            "cv_text": cv_text,
            "scraped_text": scraped_text,
            "context": context
        },
        return_only_outputs=True
    )
    
    return response["output_text"], context