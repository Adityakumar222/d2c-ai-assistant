from fastapi import FastAPI
from pydantic import BaseModel
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

class Request(BaseModel):
    query: str

SYSTEM_PROMPT = """
You are an expert D2C e-commerce growth consultant.

Analyze merchant input and give:
- Pricing suggestions
- Marketing improvements
- Profit optimization tips

Return response in this format:
Pricing:
Marketing:
Profit:
"""

@app.get("/")
def home():
    return {"message": "D2C AI Assistant Running"}

@app.post("/analyze")
async def analyze(req: Request):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": req.query}
            ]
        )

        return {"result": response.choices[0].message.content}

    except Exception as e:
        return {"error": str(e)}
