# Build checkpoint

## Works now
- proposal.md path: [link](capstone_docs\proposal.md)
- skill_matrix.md path: [link](capstone_docs\skill_matrix.md)
- Tests: `pytest -q` → 8 passed, 1 deselected (integration); security smoke → 3 passed.
- Eval: `run_eval.py` golden set → 6/6 = 1.00.
- Fixture: 300 synthetic rows; `diagnose_fixture.py` → "all rows agree with router".
- Triage API (FastAPI, :8080): `/health` 200, JWT `/token`, rate limiting, PII redaction; logistics MCP on :8006.
- Docker Compose builds 3 services (agent, mcp, triage); CI runs ruff + pytest on push/PR.

## Incident note (Tuesday diagnosis drill)
- Broke T-002's label on purpose, pytest caught it, restored the correct label.

## Deferred
- Integration and perf tests are skipped by default; they need the live stack (p95 2.08s is a laptop stub, not an SLA).
- No cloud deployment yet: runs locally with Docker only.
- Logistics data is a stub (`clinics.json`), not a live stock or routes database.

