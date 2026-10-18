# secure_triage_api.py - the triage service with the door locked
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from modules.auth import check_password, create_token, current_user
from modules.rate_limit import check_rate_limit
from agents.tools.logistics import run_logistics_agent
import os
import httpx
import uuid
import logging
from dotenv import load_dotenv

from modules.redactor import mask_pii

load_dotenv()  # Load environment variables from .env file

app = FastAPI(title="AfyaPlus Triage API (Security Inbuilt)", version="1.1.0")

LLM_GATEWAY_URL = os.environ["LLM_GATEWAY_URL"]


class AskRequest(BaseModel):
    question: str = Field(min_length=5, max_length=500)
    
class LoginRequest(BaseModel):
    username: str
    password: str

class TriageRequest(BaseModel):
    patient_message: str = Field(min_length=5, max_length=1000)
    county: str = Field(min_length=2, max_length=40)

@app.get("/health")
def health():
    return {"service": "triage-api", "version": "1.1.0", "status": "ok"}

@app.post("/token")
def login(body: LoginRequest):
    if not check_password(body.username, body.password):
        raise HTTPException(status_code=401, detail="Wrong username or password.")
    return {"access_token": create_token(body.username), "token_type": "bearer"}

@app.post("/triage")
def triage(request: TriageRequest, user: dict = Depends(current_user)):
    check_rate_limit(user["sub"])

    compliant_request = mask_pii(request.patient_message)
    try:
        response = httpx.post(
            f"{LLM_GATEWAY_URL}/health-tip",
            json=
                {"patient_message": compliant_request,
             "county": request.county
             },
            timeout=30.0,
        )
    except httpx.RequestError:
        raise HTTPException(503, "The model is unavailable. Please try again shortly.")

    if response.status_code == 503:
        raise HTTPException(503, "The model is unavailable. Please try again shortly.")
    if response.status_code >= 400:
        raise HTTPException(502, "Upstream error.")

    # append user
    result = response.json()
    result["handled_for"] = user["sub"]
    return result

@app.post("/ask-logistics")
async def ask_logistics(body: AskRequest, user: dict = Depends(current_user)):
    trace_id = str(uuid.uuid4())[:8]
    logging.info("trace=%s user=%s question=%r", trace_id, user["sub"], body.question)
    answer = await run_logistics_agent(body.question)   # wraps Lab 2's agent
    return {"question": body.question, "answer": answer, "asked_by": user["sub"]}

  