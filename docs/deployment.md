# Deployment

AfyaPlus runs as three services: triage API (8080), LLM gateway / agent (8001) and logistics MCP server (8006).

## Part A — Local deployment

### Run locally
Install dependencies with `pip install -r requirements.txt`, then start each service from the project root in its own terminal, MCP and gateway first:
```bash
python services/mcp/logistics_mcp.py
uvicorn agents.tools.triage:app --port 8001
uvicorn services.triage.app:app --port 8080
```

### Env vars
Copy `.env.example` to `.env` in the project root and fill in the values. Set `LLM_GATEWAY_URL=http://localhost:8001` and `MCP_URL=http://localhost:8006/mcp`. Also set `JWT_SECRET`, `LLM_BASE_URL` (e.g. `http://localhost:11434/v1` for Ollama), `LLM_API_KEY`, `LLM_MODEL` and `AGENT_TRIAGE_PROMPT_VERSION=1.1.0`.

### Health
`GET http://localhost:8080/health` and `GET http://localhost:8001/health` should both return 200. The gateway returns 503 `degraded` if the prompt version or hash does not match `services/triage/prompts/pin.json`.

### Fallback
There is no stub mode, so if the LLM is unreachable `/triage` returns 503 and the API stays up. Start Ollama (or set a valid hosted-model key) and retry.

## Part B — Containerised deployment

### Run with Docker Compose
Build and start all three containers from the project root:
```bash
docker compose up --build -d
docker compose ps
```
Stop them with `docker compose down`.

### Env vars
Compose reads `config/app.env` (triage API) and `config/agent.env` (gateway); the variables are the same as in Part A. Use service names instead of localhost: `LLM_GATEWAY_URL=http://agent:8001` and `MCP_URL=http://mcp:8006/mcp`. To reach Ollama on your machine, set `LLM_BASE_URL=http://host.docker.internal:11434/v1`.

### Health
Docker checks the `/health` endpoints of the triage and agent containers every 30 seconds; `docker compose ps` shows the result. Check manually with `curl localhost:8080/health` and `curl localhost:8001/health`, and debug with `docker compose logs <service>`.

### Fallback
If Docker is not available, use Part A instead and record the containerised steps as "not executed live". The agent and triage containers are each limited to 1 CPU / 512 MB, so if one is killed for running out of memory, raise the `deploy.resources` limits in `docker-compose.yml`.
