from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from firecrawl import FirecrawlApp
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()

api_keyf = os.getenv("FIRECRAWL_API")

model = FirecrawlApp(api_key=api_keyf)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, you can restrict it later
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

class URLRequest(BaseModel):
    url: str


@app.post("/processText/")
async def process_text(request: URLRequest):
    url = request.url
    result = model.crawl_url(
        url,
        params={
            'limit': 1,
            'scrapeOptions': {'formats': ['markdown', 'html']}
        },
        poll_interval=30
    )

    return {"query_received": url, "response": result}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9090, reload=True)