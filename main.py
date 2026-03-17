from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Request model
class Request(BaseModel):
    query: str

# Home route
@app.get("/")
def home():
    return {"message": "D2C AI Assistant Running"}

# Analyze route (FINAL STABLE VERSION)
@app.post("/analyze")
async def analyze(req: Request):
    query = req.query.lower()

    # default responses
    pricing = "Test price range ₹399–₹499 to improve conversions."
    marketing = "Improve ad creatives and test different audience targeting."
    profit = "Reduce wasted ad spend and focus on high ROI campaigns."

    # logic-based improvements
    if "low conversion" in query or "low sales" in query:
        marketing = "Your conversion is low → improve landing page, product images, reviews, and trust signals."

    if "high ads" in query or "ads spend" in query or "10k" in query:
        profit = "Your CAC is high → optimize targeting, reduce wasted ads, and focus on best-performing campaigns."

    if "high price" in query or "expensive" in query:
        pricing = "Your price may be too high → test discounts, bundles, or ₹399–₹499 range."

    if "low traffic" in query:
        marketing = "Your traffic is low → increase ad reach, improve SEO, and test influencer marketing."

    if "high competition" in query:
        marketing = "High competition → differentiate with branding, offers, and unique value proposition."

    return {
        "result": f"Pricing: {pricing}\nMarketing: {marketing}\nProfit: {profit}"
    }
