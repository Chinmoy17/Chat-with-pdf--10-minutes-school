from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from rag_core import retrieve_and_answer, get_pdf_text, get_text_chunks, get_vector_store
import shutil
import os

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

@app.post("/ask")
def ask_question(request: QueryRequest):
    answer, context = retrieve_and_answer(request.question)
    return {"answer": answer, "context": context}

@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    # Save uploaded PDF to disk
    file_location = f"uploaded_{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # Process PDF and update vector store
    raw_text = get_pdf_text([file_location])
    text_chunks = get_text_chunks(raw_text)
    get_vector_store(text_chunks)
    # Optionally, remove the file after processing
    os.remove(file_location)
    return {"message": "PDF processed and vector store updated."}