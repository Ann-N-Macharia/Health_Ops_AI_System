# llm_gateway.py
import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from enum import Enum
from pydantic import BaseModel, Field
from openai import OpenAI
from dotenv import load_dotenv

#Local modules
from modules.prompt_loader import load_prompt, load_pin

load_dotenv()

#ENV VARIABLES:
PROMPT_VERSION = os.environ.get('AGENT_TRIAGE__PROMPT_VERSION')
HEALTH_TIP_MODEL = os.environ["LLM_MODEL"]
HEALTH_TIP_MAX_TOKENS = 60
HEALTH_TIP_TEMPERATURE = 0.

#Prompt validation - Load and validate the prompt from the prompts directory

# prompt path
PROMPTS_DIR = Path('prompts')
HEALTH_TIP_SYSTEM_PROMPT = load_prompt('agent_triage', PROMPT_VERSION)[0]
HEALTH_TIP_SYSTEM_PROMPT_HASH = load_prompt('agent_triage', PROMPT_VERSION)[1]

#load pin
pin = load_pin()["agent_logistics_prompt"]
PINNED_VERSION = pin.get('version')
PINNED_HASH = pin.get('prompt_sha256')

#Checks
ok_hash = (PINNED_HASH==HEALTH_TIP_SYSTEM_PROMPT_HASH)
ok_version = (PINNED_VERSION==PROMPT_VERSION)



app = FastAPI(title="AfyaPlus LLM Gateway", version="1.0.0")

# client = OpenAI(api_key=os.environ["LLM_API_KEY"])

client = OpenAI(
    base_url=os.environ["LLM_BASE_URL"],
    api_key=os.environ["LLM_API_KEY"]
)



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
    if not ok_hash or not ok_version:
        raise HTTPException(
            status_code=503,
            detail={
                'status': 'degraded',
                'prompt_version': PROMPT_VERSION,
                'prompt_sha256': HEALTH_TIP_SYSTEM_PROMPT_HASH,
                'hash_match': ok_hash,
                'version_match': ok_version,
            }
        )

    return {
    'status': 'ok',
    'prompt_version': PROMPT_VERSION,
    'prompt_sha256': HEALTH_TIP_SYSTEM_PROMPT_HASH,
    'model': os.environ.get('LLM_MODEL', 'gpt-4o-mini'),
}


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