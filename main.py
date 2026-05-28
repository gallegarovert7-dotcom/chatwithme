import os
import uvicorn  # <-- FIXED: Added missing import
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
from google.genai import types

app = FastAPI()

# --- GEMINI API CONFIGURATION ---
api_key = "AIzaSyBrRZt4gA57IyENahtC4Ib-GCEVAlEF89A"

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing!")

# Initialize the Gemini Client with your key
client = genai.Client(api_key=api_key)

# Request schema for incoming Android data
class ChatRequest(BaseModel):
    message: str

# Root route to quickly verify the server is alive
@app.get("/")
def read_root():
    return {"status": "Backend is running successfully! Send POST requests to /chat"}

@app.post("/chat")
def ask_gemini(request: ChatRequest):
    try:
        # Generate content using the recommended gemini-2.5-flash model
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=request.message,
        )
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Fallback to 8000 locally, but use Railway's PORT env variable online
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)