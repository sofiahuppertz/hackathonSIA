import os
import json 
from typing import List, Dict, Iterator
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from backend.fiche_client_agent import run_workflow

load_dotenv()

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

class Collectivity(BaseModel):
  name: str

  
@app.post("/gen_fiche_client", response_model=Dict[str, str])
async def generate_fiche_client(input: Collectivity):
    try:
        # Pass the collectivity name from the request to run_workflow.
        state = await run_workflow({"collectivite": input.name})
        return {"fiche_client": state.get("fiche_client")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
           
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)