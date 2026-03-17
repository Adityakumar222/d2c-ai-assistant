from fastapi import FastAPI
from pydantic import BaseModel
import os
import requests

app = FastAPI()

# Request model
class Request(BaseModel):
    query: str

# HuggingFace API key
HF_API_KEY = os.getenv("HF_API_KEY")

# Home route
@app.get("/")
def home():
    return {"message": "D2C AI Assistant Running"}

# Analyze route
@app.post("/analyze")
async def analyze(req: Request):
    prompt = f"""
You are a D2C e-commerce expert.

Give short and clear suggestions in this format:

Pricing:
Marketing:
Profit:

Input:
{req.query}
"""

    response = requests.post(
        "https://api-inference.huggingface.co/models/google/flan-t5-large",
        headers={
            "Authorization": f"Bearer {HF_API_KEY}"
        },
        json={
            "inputs": prompt
        }
    )

    result = response.json()

    # Clean output
    if isinstance(result, list):
        output = result[0].get("generated_text", "")
    else:
        output = str(result)

    return {"result": output}
