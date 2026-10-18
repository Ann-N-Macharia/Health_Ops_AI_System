#!/usr/bin/env python3
"""Change for your project: nothing. Generates a generic labelled-record fixture.
Usage: python scripts/make_fixture.py --rows 300 --out fixtures/triage_messages_sample.jsonl
"""
import argparse
import json
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent

random.seed(11)
TEMPLATES = {
    "triage": ["symptom check", "general question", "follow-up needed"],
    "ask-logistics": ["track delivery", "shipment delay", "where is my order"]
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", type=int, default=300)
    ap.add_argument("--out", default=ROOT / "capstone_docs/fixtures/triage_messages_sample.jsonl")
    args = ap.parse_args()

    labels = list(TEMPLATES.keys())
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w") as f:
        # keep gold ids T-001..T-003 stable for tests
        gold = [
            {"id": "T-001", "text": "fever", "label": "triage"},
            {"id": "T-002", "text": "track delivery", "label": "ask-logistics"},
        ]
        for row in gold:
            f.write(json.dumps(row) + "\n")
        for i in range(3, args.rows + 1):
            label = random.choice(labels)
            text = random.choice(TEMPLATES[label])
            f.write(json.dumps({"id": f"T-{i:03d}", "text": text, "label": label}) + "\n")
    print(f"wrote {args.rows} rows to {out_path}")


if __name__ == "__main__":
    main()
