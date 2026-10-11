# llm_gateway.py
import os
from fastapi import FastAPI, HTTPException
from enum import Enum
from pydantic import BaseModel, Field
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AfyaPlus LLM Gateway", version="1.0.0")

# client = OpenAI(api_key=os.environ["LLM_API_KEY"])

client = OpenAI(
    base_url=os.environ["LLM_BASE_URL"],
    api_key=os.environ["LLM_API_KEY"]
)

# --- All agent config lives here. One place. ---

HEALTH_TIP_SYSTEM_PROMPT = (
    """You are a triage assistant for community health workers in Kenya.

Given a patient message and a county, return a JSON object with exactly two fields:

- "urgency": one of "low", "medium", "high".
    low    = self-care at home, monitor
    medium = see a clinician within 24-48 hours
    high   = seek care immediately / emergency

- "advice": one or two short sentences of non-diagnostic guidance, appropriate
    for the county context. Do not name a specific disease. Do not prescribe
    medication. Do not ask follow-up questions.

Return ONLY the JSON object. No prose, no markdown fences."""
)

HEALTH_TIP_MODEL = os.environ["LLM_MODEL"]
HEALTH_TIP_MAX_TOKENS = 60
HEALTH_TIP_TEMPERATURE = 0.7

# -------------------------------------------------

class HealthTipRequest(BaseModel):
    patient_message: str = Field(min_length=5, max_length=1000)
    county: str = Field(min_length=2, max_length=40)

class Urgency(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class HealthTipResponse(BaseModel):
    urgency: Urgency
    advice: str
   

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/health-tip", response_model=HealthTipResponse)
def health_tip(body: HealthTipRequest):
    try:
        response = client.chat.completions.create(
            model=HEALTH_TIP_MODEL,
            messages=[
                {"role": "system", "content": HEALTH_TIP_SYSTEM_PROMPT},
                {"role": "user", "content": f"health tip about: {body.patient_message} coming from a patient from {body.county}"},
            ],
            max_tokens=HEALTH_TIP_MAX_TOKENS,
            temperature=HEALTH_TIP_TEMPERATURE,
            response_format={"type": "json_object"},   # ← enforce JSON
        )
    except Exception:
        raise HTTPException(503, "The model is unavailable. Please try again shortly.")
    
    raw = response.choices[0].message.content

    try:
        parsed = HealthTipResponse.model_validate_json(raw)
    except Exception:
        # Model returned valid JSON but wrong shape, or invalid JSON entirely.
        raise HTTPException(502, "The model returned an unusable response.")

    return parsed