"""Change for your project: nothing. Update config.json route_keywords instead."""
from agents.router import route


def test_route_logistics():
    assert route("track delivery") == "ask-logistics"


def test_route_default():
    assert route("general question") == "triage"
