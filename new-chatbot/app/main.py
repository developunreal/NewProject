from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import StreamingResponse
from app.whisper import transcribe_audio
from app.db import save_chat
from langchain.llms import Ollama
from langchain.chains import ConversationChain, RetrievalQA
from langchain.memory import ConversationBufferMemory
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import TextLoader
import os

app = FastAPI()
llm = Ollama(model="llama3.2:latest")
memory = ConversationBufferMemory()
chat_chain = ConversationChain(llm=llm, memory=memory)

# Load docs for retrieval
loader = TextLoader("docs/yourfile.txt")
docs = loader.load()
embeddings = HuggingFaceEmbeddings()
db = FAISS.from_documents(docs, embeddings)
retriever = db.as_retriever()
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")
    response = chat_chain.run(prompt)
    save_chat(prompt, response)
    return {"response": response}

@app.post("/ask-doc")
async def ask_doc(request: Request):
    data = await request.json()
    question = data.get("question", "")
    answer = qa_chain.run(question)
    return {"answer": answer}

@app.post("/transcribe")
async def transcribe(file: UploadFile):
    file_path = f"temp/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    transcript = transcribe_audio(file_path)
    os.remove(file_path)
    return {"transcript": transcript}

