## Overview
AfyaPlus is an integrated AI health-operations system for partner clinics.
Its  secured FastAPI triage API (JWT login, rate limiting, PII masking) gives patients' messages an urgency level and short advice through an LLM gateway whose prompt is version-pinned. 
The same API answers logistics questions with a LangChain agent that calls tools on an MCP server for clinic stock, delivery routes and ETAs. The three services are containerised with Docker Compose, each with its own image, health check and labels for tracking cost.

## Project path
- AfyaPlus - Integrated AI health-operations system. 

## Quick start
pytest -q

## Docs
- docs/architecture.md - [link](docs\architecture.md)
- docs/deployment.md - [link](docs\deployment.md)
- docs/cost_analysis.md - [link](docs\cost_analysis.md)
- docs/user_guide.md - [link](docs\user_guide.md)
- docs/build_checkpoint.md - [link](docs\build_checkpoint.md)

## Testing
- unit default: pytest -q
- integration: pytest -m integration
- security: pytest tests/test_security_smoke.py

## Demo
Three commands: start the service, curl /health, curl /triage. See docs/user_guide.md.

### Local (bash, from project root, `.env` filled in)
```bash
python services/mcp/logistics_mcp.py & uvicorn agents.tools.triage:app --port 8001 & uvicorn services.triage.app:app --port 8080 &
curl localhost:8080/health
curl -X POST localhost:8080/triage -H "Content-Type: application/json" -H "Authorization: Bearer $(curl -s -X POST localhost:8080/token -H 'Content-Type: application/json' -d '{"username":"$USERNAME","password":"$PASSWORD"}' | python -c 'import sys,json;print(json.load(sys.stdin)["access_token"])')" -d '{"patient_message":"I have had a fever for two days","county":"Kisumu"}'
```

### Dockerised (`config/app.env` and `config/agent.env` filled in)
```bash
docker compose up --build -d
curl localhost:8080/health
curl -X POST localhost:8080/triage -H "Content-Type: application/json" -H "Authorization: Bearer $(curl -s -X POST localhost:8080/token -H 'Content-Type: application/json' -d '{"username":"mercy","password":"logistics2026"}' | python -c 'import sys,json;print(json.load(sys.stdin)["access_token"])')" -d '{"patient_message":"I have had a fever for two days","county":"Kisumu"}'
```
Expected: `/health` returns `{"service": "triage-api", "status": "ok", ...}` and `/triage` returns `{"urgency": "...", "advice": "...", "handled_for": "mercy"}`.

## Presentation
docs/presentation.pdf, presented Week 12 Monday.

## Peer review
- review_log.md entry:
- checklist: docs/peer_review_checklist.md

## Fallbacks declared
- [ ] no live OpenAI key (stub agent)
- [ ] no Docker (integration manual)
- [ ] no cloud deploy executed (docs only)
- [ ] solo reviewer (self-review with checklist)

## Submission checklist
- [ ] proposal + skill_matrix + map
- [ ] five docs linked
- [ ] peer review completed
- [ ] slides PDF in docs/ and demo command documented