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

class SourceMaterialSchema(BaseModel):
    summary: str
    key_points: str
    content_type: str 

@app.post("/processText/")
async def process_text(request: URLRequest):
    url = request.url
    result = model.extract(
        [ url],
     {
        'prompt': (
            "Read the content and extract: "
            "1. A brief summary of what the page is about, "
            "2. Key points or highlights, "
            "3. What kind of content it is (e.g., document, research data, blog draft, product specs, course outline)."
        ),
        'schema': SourceMaterialSchema.model_json_schema()
    }
    )

    return {"query_received": url, "response": result}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9090, reload=True)