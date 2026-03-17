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

    try:
        response = requests.post(
            "https://router.huggingface.co/hf-inference/models/google/flan-t5-large",
            headers={
                "Authorization": f"Bearer {HF_API_KEY}"
            },
            json={
                "inputs": prompt
            }
        )

        # Debug (optional)
        # print(response.text)

        data = response.json()

        # Handle proper output
        if isinstance(data, list):
            output = data[0].get("generated_text", "")
        elif "error" in data:
            output = f"Model error: {data['error']}"
        else:
            output = str(data)

        return {"result": output}

    except Exception as e:
        return {"error": str(e)}
