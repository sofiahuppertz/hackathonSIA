import sys
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from srcs.client_sheet_generator_agent import run_workflow
from schemas import ClientRequest
import httpx
import urllib.parse

load_dotenv()

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

@app.post("/gen_client_sheet")
async def gen_client_sheet(input: ClientRequest):
    try:
        state = await run_workflow(input.region)
        response_data = {
            "content": state.get("fiche_client", ""),
            "images": state.get("images", []),
            "urls": state.get("web_sources", []),
        }
        return response_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/proxy")
async def proxy(url: str):
    # Decode the URL parameter
    decoded_url = urllib.parse.unquote(url)
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(decoded_url)
    except httpx.RequestError as exc:
        raise HTTPException(status_code=500, detail=f"Error fetching {decoded_url}: {exc}")

    # Create a new header dict without the security headers
    headers = dict(response.headers)
    # headers.pop("X-Frame-Options", None)
    # headers.pop("Content-Security-Policy", None)
    
    return Response(
        content=response.content,
        media_type=response.headers.get("content-type", "text/html"),
        headers=headers
    )