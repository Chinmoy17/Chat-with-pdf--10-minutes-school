# PDF-ALAP  
## Multilingual PDF & Image Chatbot (RAG System)

![Demo Screenshot](general.png)

## About the Project

**PDF-ALAP** is a privacy-focused, multilingual chatbot that lets you interact with your own PDF and image documents—extracting, searching, and answering questions in both Bangla and English.  
It’s designed for anyone who needs fast, secure, and accurate information retrieval from large or complex documents, including scanned files.

**Why this project?**  
Built from scratch to solve the real problem of searching and understanding information locked inside PDFs and images—without sending your data to the cloud.  
It’s ideal for students, educators, researchers, HR, legal, and anyone who values data privacy.

---

## Key Features

- **Multilingual Support:** Ask and get answers in Bangla or English.
- **Works with Any PDF or Image:** Handles both text-based and scanned/image-based documents using OCR.
- **Data Privacy:** All processing is local—your documents and questions never leave your machine.
- **Advanced Text Cleaning:** Removes noise, preserves structure (like MCQs), and normalizes text for best results.
- **Semantic Search:** Uses state-of-the-art vector search (FAISS) and embeddings for accurate retrieval.
- **Conversational Memory:** Remembers your chat history for a natural Q&A experience.
- **Modern Chatbot UI:** Streamlit-based interface for easy, interactive use.
- **REST API:** FastAPI backend for integration with other apps or automation.
- **Evaluation Tools:** Built-in scripts to measure answer quality and relevance.
- **Flexible Use Cases:** Education, resume comparison, legal document search, and more.

---

## How It Works

1. **Upload** one or more PDFs (text or scanned).
2. **Ask** questions in Bangla or English—about facts, MCQs, summaries, etc.
3. **Get Answers** instantly, grounded in your documents.
4. **All data stays on your device**—no cloud upload, no third-party sharing.

---

## Getting Started

### 1. Install Dependencies
```sh
pip install -r [requirements.txt](http://_vscodecontentref_/2)
```
### 2.Set Up Environment Variables
Create a .env file with your Google API key:
```
GOOGLE_API_KEY=your_google_api_key_here
```

### 
Install Tesseract OCR on your system.
Add the Tesseract executable path in your code before using pytesseract:
```
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```
### 4.Run the Streamlit App
```
streamlit run app.py
```
Use the sidebar to upload your PDF(s).
Chat with your documents in Bangla or English

### 5. Run the FAST API
```
uvicorn api:app --reload
```
Access the API docs at http://127.0.0.1:8000/docs
Use /upload_pdf/ to upload a PDF and /ask to ask questions.

Data Security & Privacy
Local Processing: All document parsing, embedding, and retrieval happen on your machine.
No Cloud Upload: Your files and questions are never sent to any server or third party.
Open Source: Review and modify the code as you wish.
Example Use Cases
Education: Instantly answer questions from textbooks, notes, or exam papers.
Resume/Document Comparison: Find and compare information across multiple PDFs.
Legal/Research: Search and summarize large legal or research documents.
MCQ Extraction: Count and retrieve multiple-choice questions from scanned or digital papers.

Credits
Built from scratch by [Your Name]

Designed, coded, and tested all core modules (OCR, chunking, vector search, LLM integration, UI, API, evaluation).
Special thanks to the open-source community for tools like Streamlit, FastAPI, FAISS, and Tesseract.
Improvements & Roadmap
MCQ/CQ mode for specialized question types.
More advanced chunking (paragraph, MCQ-aware).
Enhanced document comparison features.
Cloud/server deployment options (optional).
More language support and embedding models.
License
This project is open source and free to use under the MIT License.

Feel free to fork, contribute, or reach out for collaboration!
