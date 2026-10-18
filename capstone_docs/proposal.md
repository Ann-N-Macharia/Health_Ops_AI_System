# Capstone proposal
## Path
AfyaPlus Module 4 Capstone: integrated AI health-operations system

## Problem
AfyaPlus, a network of healthcare facilities, faces challenges in timely patient prioritization and coordinating logistics across locations. Limited visibility into stock availability and routes can delay care and resource allocation.

The AfyaPlus Integrated health operations systems is an AI powered solution that enhnaces both **clinical** and **logistics** operations managament.

Under **clinical operations**, the system receives medical queries from patients in different counties, its then rank urgency of the issue and recommend next best steps. No diagnosis is provided.

Under **logistics operations** the  solution also handles queries on matters logistics. Its MCP servers access a stub database for stock, routes, distances across the Afyaplus network.

Decisions supported by the solution include:

- Routing of medical cases depending on urgency.
- Logistics planning.

To know the system is working well:

- **For clinical uses** 

    - The system should provide an urgency level for the case provided.
    - Provide next best recommended steps for the case and not diagnose or prescribe any medication

- **For logistics management:**

    - The system should provide accurate information on stock count, locations distances 
    - The responses should not contain hallucinated figures. If it has no access to information of a specific product that should be the output and not made up figures.

## Dataset
fixtures/triage_messages_sample.jsonl: ~300 synthetic rows (teaching only).
Do not scrape production. Do not use millions of rows.

## Milestones
- Monday: proposal, skill_matrix, integration_map, base service /health 200
- Tuesday: pytest pyramid, security smoke, CI, remaining layers, fixture diagnosis, eval score
- Thursday: docs, peer review, presentation deck
- Week 12 Monday: presentation and demo

## Out of scope
- Training a new foundation model
- Live crawl of PII
- Mixing clinical and marketplace fixtures
