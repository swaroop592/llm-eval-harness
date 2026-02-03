import time
import re
from .base import LLMProvider

def _doc_and_question(prompt: str):
    parts = prompt.split("\n\nQuestion:", 1)
    doc = parts[0] if parts else prompt
    q = parts[1].strip() if len(parts) == 2 else ""
    return doc, q

class KeywordProvider(LLMProvider):
    """
    Deterministic baseline that extracts short answers by pattern rules.
    More general than MockProvider, still explainable.
    """

    def generate(self, prompt: str):
        start = time.time()
        doc, q = _doc_and_question(prompt)
        ql = q.lower()

        answer = "NOT_FOUND"
        evidence = ""

        patterns = []

        # Add a few generic patterns
        if "how many days" in ql or "within how many days" in ql:
            patterns = [r"within (\d+)\s+days", r"(\d+)\s+days of purchase"]
        elif "uptime target" in ql:
            patterns = [r"uptime target:\s*([\d.]+%)", r"target is\s*([\d.]+%)"]
        elif "carry over" in ql:
            patterns = [r"carry over up to (\d+\s+days)"]
        elif "retry" in ql:
            patterns = [r"no more than (\d+)\s+times"]

        for pat in patterns:
            m = re.search(pat, doc, flags=re.IGNORECASE)
            if m:
                val = m.group(1).strip()
                # Create minimal evidence snippet
                answer = val if "%" in val or "day" in val or val.isdigit() else val
                # evidence = the matched sentence-ish
                span_start = max(0, m.start() - 60)
                span_end = min(len(doc), m.end() + 60)
                evidence = doc[span_start:span_end].strip()
                break

        time.sleep(0.01)
        latency_ms = (time.time() - start) * 1000

        return {
            "answer": answer,
            "evidence": evidence,
            "confidence": 0.4,
            "latency_ms": latency_ms,
            "prompt_tokens": len(prompt.split()),
            "completion_tokens": max(3, len(str(answer).split())),
        }
