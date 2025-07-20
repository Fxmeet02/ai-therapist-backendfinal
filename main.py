from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import openai
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = "YOUR_OPENAI_API_KEY"

@app.get("/")
def root():
    return {"message": "Backend is working"}

@app.post("/analyze_emotion")
async def analyze_emotion(text: str = Form(...)):
    response = openai.ChatCompletion.create(
        model="gpt-4o-preview",
        messages=[
            {"role": "system", "content": "You are an emotion detector. Return the dominant emotion in one word."},
            {"role": "user", "content": text}
        ]
    )
    return {"emotion": response.choices[0].message.content.strip()}

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    transcript = openai.Audio.transcribe("whisper-1", file.file)
    return {"transcript": transcript["text"]}

@app.post("/journal")
async def post_journal(entry: str = Form(...)):
    return {"status": "saved", "entry": entry}

@app.get("/journal")
async def get_journal():
    return {"entries": []}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10000, reload=True)
