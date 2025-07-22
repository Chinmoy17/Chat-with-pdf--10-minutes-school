# Multilingual PDF Chatbot (RAG System)

## About the Project

This project is a **Retrieval-Augmented Generation (RAG) system** designed to answer questions in both English and Bangla from a PDF document corpus. It combines state-of-the-art document retrieval with large language models to provide accurate, context-grounded answers to user queries.

**Key Features:**
- Multilingual support (Bangla & English)
- PDF knowledge base (text and scanned/image PDFs)
- Advanced text cleaning and OCR
- Semantic chunking and vector search (FAISS)
- Conversational memory (chat history)
- Streamlit chatbot UI and REST API (FastAPI)
- Evaluation tools for answer quality

---

## How to Run the Project

### 1. **Install Dependencies**
```sh
pip install -r requirements.txt
```

### 2. **Set Up Environment Variables**
- Create a `.env` file with your Google API key:
  ```
  GOOGLE_API_KEY=your_google_api_key_here
  ```

### 3. **Set Up Tesseract Path**
- Install [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) on your system.
- Add the Tesseract executable path in your code before using pytesseract:
  ```python
  import pytesseract
  pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
  ```
  (Adjust the path if you installed Tesseract elsewhere.)

### 4. **Run the Streamlit App**
```sh
streamlit run app.py
```
- Use the sidebar to upload your PDF(s).
- Ask questions in Bangla or English in the chat interface.

### 5. **Run the REST API (Optional)**
```sh
uvicorn api:app --reload
```
- Access the API docs at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Use `/upload_pdf/` to upload a PDF and `/ask` to ask questions.

### 6. **Run Evaluation (Optional)**
```sh
python evaluation.py
```
- See tabular results and summary metrics for sample queries.

---

## Task Completion & Answers to Assessment Questions

### **How the Task is Completed**
- The system accepts queries in both English and Bangla.
- It retrieves relevant chunks from a vectorized PDF knowledge base (using FAISS).
- Answers are generated using a Gemini LLM, grounded in the retrieved context.
- Both long-term (vector DB) and short-term (chat history) memory are maintained.
- The app supports both text-based and scanned PDFs (via OCR).
- Evaluation scripts and a REST API are included for completeness.

### **Assessment Questions**

**1. What method or library did you use to extract the text, and why? Did you face any formatting challenges with the PDF content?**  
- Used `pdfplumber` for text-based PDFs and `pytesseract` (OCR) for scanned/image-based PDFs.  
- Formatting challenges included page numbers, headers/footers, and line breaks, which were addressed with regex-based cleaning.

**2. What chunking strategy did you choose (e.g. paragraph-based, sentence-based, character limit)? Why do you think it works well for semantic retrieval?**  
- Used character-based chunking with overlap (e.g., 1024 chars, 300 overlap).  
- This ensures context is preserved and relevant information is not split across chunks, improving semantic retrieval.

**3. What embedding model did you use? Why did you choose it? How does it capture the meaning of the text?**  
- Used Google’s `models/embedding-001` for multilingual support and strong semantic understanding.  
- It captures the meaning of both Bangla and English text, enabling effective cross-language retrieval.

**4. How are you comparing the query with your stored chunks? Why did you choose this similarity method and storage setup?**  
- Used FAISS for vector storage and cosine similarity for retrieval.  
- FAISS is efficient for large-scale vector search, and cosine similarity is standard for semantic comparison.

**5. How do you ensure that the question and the document chunks are compared meaningfully? What would happen if the query is vague or missing context?**  
- By using semantic embeddings and overlapping chunks, the system compares the true meaning of queries and chunks.  
- If the query is vague or missing context, the system may retrieve less relevant chunks or respond that the answer is not available in the context.

**6. Do the results seem relevant? If not, what might improve them (e.g. better chunking, better embedding model, larger document)?**  
- Results are generally relevant for well-formed queries.  
- Improvements could include paragraph/MCQ-based chunking, more advanced cleaning, or using a larger/more specialized embedding model.

---

## Notes

- **Tesseract Path:**  
  Make sure to set the correct path for Tesseract OCR in your code as shown above.
- **Sample Queries:**  
  - অনুপমের ভাষায় সুপুরুষ কাকে বলা হয়েছে?
  - কাকে অনুপম ভাগ্য দেবতা বলে উল্লেখ করা হয়েছে?
  - বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?
- **API Documentation:**  
  See FastAPI docs at `/docs` after running the API.

---

