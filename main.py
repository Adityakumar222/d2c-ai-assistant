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
            },
            timeout=30
        )

        # Handle empty response
        if not response.text or response.text.strip() == "":
            return {"error": "Empty response from model. Retry."}

        # Try parsing JSON safely
        try:
            data = response.json()
        except:
            return {"error": "Invalid response from model."}

        # Handle different cases
        if isinstance(data, list):
            output = data[0].get("generated_text", "")
        elif isinstance(data, dict) and "error" in data:
            return {"error": data["error"]}
        else:
            output = str(data)

        return {"result": output}

    except requests.exceptions.Timeout:
        return {"error": "Request timeout. Try again."}
    except Exception as e:
        return {"error": str(e)}
