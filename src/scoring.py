import re

def normalize(text: str) -> str:
    if text is None:
        return ""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text


def is_correct(predicted: str, expected: str) -> bool:
    return normalize(predicted) == normalize(expected)
