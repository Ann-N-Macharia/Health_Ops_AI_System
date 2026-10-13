"""Load a versioned triage system prompt from prompts/."""
from pathlib import Path
import hashlib
import json

PROMPTS_DIR = Path('prompts')


def load_prompt(name: str, version: str) -> str:
    path = PROMPTS_DIR / f'{name}_v{version}.txt'
    if not path.is_file():
        raise FileNotFoundError(f'No prompt for version {version!r}: {path}')
    prompt = path.read_text(encoding='utf-8')
    prompt_hash = hashlib.sha256(prompt.encode()).hexdigest()
    return prompt, prompt_hash

def load_pin(path: str = 'PROMPTS_DIR / pin.json') -> dict:
    with open(path) as f:
        return json.load(f)


#testing
if __name__ == '__main__':
    text = load_prompt('agent_logistics', '1.1.0')
    print('chars', len(text))
