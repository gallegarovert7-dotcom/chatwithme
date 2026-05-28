import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai

app = FastAPI()

# --- GEMINI API CONFIGURATION ---
# Safely reads the key from Vercel's Environment Variables
api_key = os.environ.get("GEMINI_API_KEY")


# Request schema for incoming data
class ChatRequest(BaseModel):
    message: str


@app.get("/")
def read_root():
    return {"status": "Backend is running!"}


@app.post("/chat")
def ask_gemini(request: ChatRequest):
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY environment variable is missing on Vercel!")

    try:
        # Initialize client inside the route or globally
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=request.message,
        )
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))