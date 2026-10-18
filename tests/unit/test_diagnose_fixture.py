import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FIXTURE = PROJECT_ROOT / "capstone_docs" / "fixtures" / "triage_messages_sample.jsonl"


def test_diagnose_fixture_runs_successfully():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "capstone_docs.scripts.diagnose_fixture",
            str(FIXTURE),
        ],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert "diagnose OK" in result.stdout
    assert "all rows agree with router" in result.stdout
    assert "FAIL disagreements" not in result.stdout