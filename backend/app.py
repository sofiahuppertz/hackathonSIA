from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from srcs.client_sheet_generator_agent import run_workflow
from schemas import ClientRequest

load_dotenv()

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

# @app.post("/gen_client_sheet")
# async def gen_client_sheet(input: ClientRequest):
#     try:
#         print(input.region)
#         state = await run_workflow(input.region)
#         print(state)
#         fiche_client = state.get("fiche_client", "")
#         async def stream_response():
#             yield fiche_client.encode("utf-8")
        
#         return StreamingResponse(stream_response(), media_type="text/plain")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

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