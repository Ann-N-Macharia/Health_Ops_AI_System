#!/usr/bin/env python3
"""Change for your project: nothing. Prints a score against evals/golden.jsonl."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))

from agents.router import route

def main():
    #Path to the goldent set.
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "capstone_docs/evals/golden.jsonl")
    print(path)

    #Read the golden set rows.
    rows = [json.loads(l) for l in path.read_text().splitlines() if l.strip()]
    correct = sum(1 for r in rows if route(r["text"]) == r["expected_label"])
    score = correct / len(rows) if rows else 0.0
    print(f"golden-set score: {correct}/{len(rows)} = {score:.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
