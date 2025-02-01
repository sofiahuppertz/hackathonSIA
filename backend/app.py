import os
import json 
from typing import List, Dict, Iterator
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

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
  
class 

  
@app.post("/chat")
async def chat_endpoint(input: Collectivity):
    try:
        talk.messages.append(
            {"role": input.role, "content": input.message}
        )
        return StreamingResponse(stream_response(), media_type="text/plain")
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=str(e)
        )
           
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)