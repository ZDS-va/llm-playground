from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
PROMPT_DIR = BASE_DIR / "prompts"

def load_prompt(prompt_name: str) -> str:
    prompt_path = PROMPT_DIR / prompt_name
    return prompt_path.read_text(encoding="utf-8")
