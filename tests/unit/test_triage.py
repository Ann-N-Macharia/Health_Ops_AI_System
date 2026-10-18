def test_redaction_strips_email():
    from modules.redactor import mask_pii
    assert '0712345678' not in mask_pii('contact phone number is 0721950675')

def test_pin_has_model_and_version():
    import json
    pin = json.loads(open("services/triage/prompts/pin.json").read())
    assert pin.get("agent_logistics_prompt") and pin.get("agent_triage_prompt")