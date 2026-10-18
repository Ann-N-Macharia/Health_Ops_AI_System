# User guide

AfyaPlus gives clinic staff two AI helpers behind one secured API: patient triage advice and logistics questions (stock, delivery routes, ETAs).

## Part A — Local use

### Run
Start the three services as described in `docs/deployment.md` (Part A). The API is then available at `http://localhost:8080`, with interactive docs at `http://localhost:8080/docs`.

### Use the API
Log in to get a 30-minute token, then send it as `Authorization: Bearer <token>` on every call:
```bash
curl -X POST localhost:8080/token -H "Content-Type: application/json" -d '{"username":"mercy","password":"logistics2026"}'
curl -X POST localhost:8080/triage -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{"patient_message":"I have had a fever for two days","county":"Kisumu"}'
curl -X POST localhost:8080/ask-logistics -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{"question":"How many units of amoxicillin are there?"}'
```
Triage returns `{"urgency": "low|medium|high", "advice": "..."}`. Phone numbers and emails in the message are masked before they reach the model.

### Health check
`curl localhost:8080/health` should return `{"service": "triage-api", "status": "ok"}`.

### Fallback path
There is no stub mode, so if the model is down you get a 503 and should retry once the LLM is back. A 401 means you need to log in again, and a 429 means you sent more than 5 requests in a minute.

### Fixture location
`capstone_docs/fixtures/triage_messages_sample.jsonl` holds about 300 synthetic triage messages. Regenerate it with `python capstone_docs/scripts/make_fixture.py --rows 300 --out capstone_docs/fixtures/triage_messages_sample.jsonl`.

## Part B — Containerised use

### Run
Start the stack with `docker compose up --build -d` (see `docs/deployment.md`, Part B). Clients talk only to the triage API on port 8080; the agent (8001) and MCP server (8006) are internal services.

### Use the API
The requests are exactly the same as in Part A, sent to `http://localhost:8080`. `python z_clients.py` runs a quick login and logistics test, but first change its `base_url` to port 8080.

### Health check
`docker compose ps` should list the triage and agent containers as `healthy`. If either is unhealthy, check `docker compose logs triage` or `docker compose logs agent`.

### Fallback path
If a container keeps restarting, it is usually a missing env value in `config/*.env` or the prompt pin check failing. Fix the value and run `docker compose up -d` again, or fall back to Part A.
