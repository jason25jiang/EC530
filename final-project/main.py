# main.py
import os
import sqlite3
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from openai import OpenAI

app = FastAPI()

# Allow CORS for frontend testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (e.g., index.html)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse("static/index.html")

# Initialize SQLite DB
conn = sqlite3.connect('db/documents.db', check_same_thread=False)
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        content BLOB
    )
''')
conn.commit()

# Setup OpenAI client (API key to be set later)
openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")  # Expecting you to set this environment variable
)

@app.get("/")
async def root():
    return {"message": "API is running. Try /upload or /analyze/{doc_id}"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()

    # Save to DB
    c.execute("INSERT INTO documents (filename, content) VALUES (?, ?)", (file.filename, content))
    conn.commit()

    return {"message": f"Uploaded {file.filename} successfully"}

@app.get("/analyze/{doc_id}")
async def analyze_document(doc_id: int):
    # Fetch document
    c.execute("SELECT content FROM documents WHERE id=?", (doc_id,))
    row = c.fetchone()
    if not row:
        return JSONResponse(status_code=404, content={"message": "Document not found"})

    content = row[0].decode("utf-8", errors="ignore")

    # Analyze with OpenAI
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful document analyzer."},
                {"role": "user", "content": f"Analyze this document:\n{content}"}
            ]
        )

        analysis = response.choices[0].message.content
        return {"analysis": analysis}

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Error: {str(e)}"})
