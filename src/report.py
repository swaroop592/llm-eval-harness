from pathlib import Path

def write_summary(path: str, text: str):
    Path(path).write_text(text, encoding="utf-8")
