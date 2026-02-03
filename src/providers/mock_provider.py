import time
import re
from .base import LLMProvider

def _extract_document(prompt: str) -> str:
    # In our runner, prompt is: "{doc}\n\nQuestion: ..."
    parts = prompt.split("\n\nQuestion:", 1)
    return parts[0] if parts else prompt

def _extract_question(prompt: str) -> str:
    parts = prompt.split("\n\nQuestion:", 1)
    return parts[1].strip() if len(parts) == 2 else ""

def _find_first_match(patterns, text):
    for pat in patterns:
        m = re.search(pat, text, flags=re.IGNORECASE | re.MULTILINE)
        if m:
            return m.group(1).strip()
    return None

class MockProvider(LLMProvider):
    """
    Deterministic, rule-based provider that extracts answers from the document text.
    This is NOT an LLM. It exists to prove reproducibility and provide a baseline.
    """

    def generate(self, prompt: str):
        start = time.time()
        doc = _extract_document(prompt)
        q = _extract_question(prompt).lower()

        answer = "NOT_FOUND"
        evidence = ""
        confidence = 0.2

        # Heuristics for common patterns in our docs
        if "refund" in q and "within how many days" in q:
            val = _find_first_match([r"within (\d+)\s+days"], doc)
            if val:
                answer = f"Within {val} days of purchase."
                evidence = f"Customers may request a refund within {val} days of purchase."
                confidence = 0.7

        elif "refund percentage" in q and "within 7 days" in q:
            val = _find_first_match([r"within 7 days.*?receive (\d+%)"], doc)
            if val:
                answer = val
                evidence = f"If a refund is approved within 7 days of purchase, customers receive {val}."
                confidence = 0.7

        elif "refund percentage" in q and "between 8" in q:
            val = _find_first_match([r"between 8–30 days.*?receive (\d+%)"], doc)
            if val:
                answer = val
                evidence = f"If approved between 8–30 days, customers receive {val}."
                confidence = 0.7

        elif "uptime target" in q:
            val = _find_first_match([r"uptime target:\s*([\d.]+%)"], doc)
            if val:
                answer = val
                evidence = f"Monthly uptime target: {val}"
                confidence = 0.7

        elif "scheduled maintenance" in q:
            val = _find_first_match([r"occurs on (Sundays.*?UTC)"], doc)
            if val:
                answer = val
                evidence = f"Scheduled maintenance occurs on {val}."
                confidence = 0.7

        elif "response time" in q and "severity 1" in q:
            val = _find_first_match([r"Severity 1:\s*response within ([^\n]+)"], doc)
            if val:
                answer = f"Within {val}."
                evidence = f"Severity 1: response within {val}"
                confidence = 0.7

        elif "vacation days per year" in q:
            val = _find_first_match([r"\((\d+\s+days/year)\)"], doc)
            if val:
                answer = val.replace("/year", " per year")
                evidence = f"Full-time employees accrue 1.25 vacation days per month ({val})."
                confidence = 0.7

        elif "carry over" in q and "vacation" in q:
            val = _find_first_match([r"carry over up to (\d+\s+days)"], doc)
            if val:
                answer = f"Up to {val}."
                evidence = f"Unused vacation may carry over up to {val} into the next calendar year."
                confidence = 0.7

        # latency + token estimates
        time.sleep(0.01)
        latency_ms = (time.time() - start) * 1000

        return {
            "answer": answer,
            "evidence": evidence,
            "confidence": confidence,
            "latency_ms": latency_ms,
            "prompt_tokens": len(prompt.split()),
            "completion_tokens": max(3, len(answer.split())),
        }
