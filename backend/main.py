from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import traceback

import os

load_dotenv()

from .agent import chat

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def read_root():
    return {"status": "ok"}


@app.post("/chat")
def chatbot(req: ChatRequest):

    try:

        print("=" * 50)
        print("Message received:", req.message)

        result = chat(req.message)

        print("Result:", result)

        return {
            "response": result
        }

    except Exception as e:

        print("\nERROR OCCURRED\n")
        traceback.print_exc()

        return {
            "error": str(e)
        }
