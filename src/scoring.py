import re

def normalize(text: str) -> str:
    if text is None:
        return ""
    text = str(text).lower().strip()
    text = re.sub(r"[^\w\s%–-]", "", text)  # keep % and dash-like chars
    text = re.sub(r"\s+", " ", text)
    return text


def is_correct(predicted: str, expected: str) -> bool:
    return normalize(predicted) == normalize(expected)


def evidence_ok(model_evidence: str, doc_text: str) -> bool:
    """
    Evidence is OK if it's non-empty and appears in the document (case-insensitive).
    """
    ev = (model_evidence or "").strip()
    if not ev:
        return False
    return normalize(ev) in normalize(doc_text)


def grade_item(
    predicted_answer: str,
    expected_answer: str,
    model_evidence: str,
    doc_text: str,
    gold_evidence: str | None = None,
):
    """
    Returns:
      - correct_answer (bool)
      - grounded (bool or None)  -> None means "not evaluated"
      - final_correct (bool)      -> answer correctness AND grounding (when applicable)
    """
    correct_answer = is_correct(predicted_answer, expected_answer)

    # If expected is NOT_FOUND, grounding doesn't apply.
    if normalize(expected_answer) == "not_found":
        return correct_answer, None, correct_answer

    # If gold evidence is provided, enforce grounding.
    if gold_evidence and str(gold_evidence).strip():
        grounded = evidence_ok(model_evidence, doc_text)
        final_correct = correct_answer and grounded
        return correct_answer, grounded, final_correct

    # Otherwise, don't enforce grounding (but we still expose that grounding wasn't checked).
    return correct_answer, None, correct_answer
