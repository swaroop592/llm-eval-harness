import pandas as pd
from pathlib import Path

RESULTS_PATH = "results/results.csv"
DOCS_DIR = "data/docs"
OUT_PATH = "reports/failure_modes.md"

def load_doc(doc_id: str) -> str:
    path = Path(DOCS_DIR) / f"{doc_id}.txt"
    return path.read_text(encoding="utf-8")

def main():
    df = pd.read_csv(RESULTS_PATH)

    # Focus on incorrect answers only
    wrong = df[df["correct"] == False].copy()
    if wrong.empty:
        Path(OUT_PATH).write_text("# Failure Modes\n\nNo failures found.\n", encoding="utf-8")
        print("No failures; wrote empty failure report.")
        return

    # Heuristic “failure categories”
    def categorize(row):
        exp = str(row["expected_answer"]).lower()
        pred = str(row["predicted_answer"]).lower()

        if pred == "not_found" and exp != "not_found":
            return "Missed answer (returned NOT_FOUND)"
        if pred != "not_found" and exp == "not_found":
            return "False positive (answered when should be NOT_FOUND)"
        if any(x in exp for x in ["%", "days", "hour", "minutes", "utc", "am", "pm"]) and pred != exp:
            return "Numeric/time mismatch"
        return "Other / rubric limitation"

    wrong["failure_mode"] = wrong.apply(categorize, axis=1)

    lines = []
    lines.append("# Failure Modes (auto-generated)\n")
    lines.append(f"Total failures: {len(wrong)}\n")

    for mode, sub in wrong.groupby("failure_mode"):
        lines.append(f"## {mode}\n")
        lines.append(f"Count: {len(sub)}\n")
        # Show up to 5 examples
        for _, r in sub.head(5).iterrows():
            lines.append(f"- **{r['id']}** ({r['doc_id']}, {r['case_type']}): "
                         f"expected='{r['expected_answer']}' | predicted='{r['predicted_answer']}'")
        lines.append("")

    Path(OUT_PATH).write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote failure modes to {OUT_PATH}")

if __name__ == "__main__":
    main()
