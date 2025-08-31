
# PDF-Alap: Your AI Research Assistant 📄✨

PDF-Alap is an AI-powered research assistant built with Streamlit and powered by Google's Gemini models. It helps students and researchers analyze academic papers, synthesize information, and draft compelling, context-aware emails for academic and funding opportunities.

## Features

- **Conversational Q&A:** Chat with your research papers to quickly find information and understand complex topics.
- **Multi-Source Context:** The application can process information from multiple sources to provide rich, contextual answers:
  - **Research Papers:** Upload PDFs directly or provide URLs from sites like arXiv.
  - **Applicant's CV:** Upload your CV to personalize email drafts.
  - **Professor's Website:** Provide a URL to a professor's website or Google Scholar profile to tailor communications.
- **AI-Powered Email Drafting:** Automatically generate professional and personalized emails for PhD inquiries, research positions, and funding requests.
- **Efficient Processing:** Utilizes a caching mechanism to ensure fast reprocessing of previously used documents and URLs.
- **Clean UI:** A modern, tabbed interface allows for easy and organized data input.

## Tech Stack

- **Frontend:** Streamlit
- **Core AI:** Python, LangChain, Google Gemini
- **Vector Storage:** ChromaDB
- **Data Processing:** pdfplumber, pytesseract, BeautifulSoup

## Setup and Installation

Follow these steps to get the application running on your local machine.

**1. Clone the Repository**
```bash
git clone <repository-url>
cd <repository-directory>
```

**2. Create a Virtual Environment (Recommended)**
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

**4. Set Up Environment Variables**

Create a file named `.env` in the root of the project directory and add your Google API key:

```
GOOGLE_API_KEY="your_google_api_key_here"
```

## How to Use

**1. Run the Application**

Open your terminal and run the following command:

```bash
streamlit run app.py
```

**2. Input Your Data**

- Use the sidebar to provide your data.
- **Upload Tab:** Upload research papers and your CV in PDF format.
- **From URL Tab:** Paste URLs to research papers and the professor's professional website.

**3. Process**

- Click the **"Submit & Process"** button. The application will ingest all the provided data, process it, and create a vector store.

**4. Interact**

- Once processing is complete, you can start interacting with the assistant in the main chat window.
- **Ask questions** about the research papers (e.g., "What is the main conclusion of the paper on quantum computing?").
- **Request an email draft** (e.g., "Write an email to Professor Smith expressing my interest in their work on machine learning.").
