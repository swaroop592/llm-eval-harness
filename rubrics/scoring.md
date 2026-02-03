Scoring Rubric (v1)

1) Correctness
- For non-NOT_FOUND answers, a prediction is correct if the normalized predicted answer matches the normalized expected answer.
- Normalization: lowercase, trim whitespace, collapse multiple spaces, remove surrounding punctuation.

2) NOT_FOUND behavior
- If expected_answer is NOT_FOUND, then predicted answer must be NOT_FOUND to be correct.

3) Evidence
- Evidence is not required for correctness in v1, but is collected for failure mode analysis.
