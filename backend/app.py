from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from srcs.client_sheet_generator_agent import run_workflow
from schemas import ClientRequest
from fastapi.encoders import jsonable_encoder
import httpx
import urllib.parse

load_dotenv()

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
            "images": state.get("section_images", []),
            "urls": state.get("section_urls", []),
        }
        return jsonable_encoder(response_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

