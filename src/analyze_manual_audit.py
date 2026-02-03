import pandas as pd
from pathlib import Path

AUDIT_PATH = "reports/manual_audit.csv"
OUT_PATH = "reports/manual_audit_summary.md"

def main():
    df = pd.read_csv(AUDIT_PATH)

    # human_correct is empty until you fill it; handle that.
    if "human_correct" not in df.columns or df["human_correct"].isna().all() or (df["human_correct"].astype(str).str.strip() == "").all():
        Path(OUT_PATH).write_text(
            "# Manual Audit Summary\n\n"
            "manual_audit.csv exists, but `human_correct` is not filled yet.\n"
            "Fill `human_correct` as True/False (or 1/0) and re-run this script.\n",
            encoding="utf-8"
        )
        print("Human audit not filled yet. Wrote placeholder summary.")
        return

    # Normalize human_correct
    def to_bool(x):
        s = str(x).strip().lower()
        return s in ["true", "1", "yes", "y"]

    df["human_correct_bool"] = df["human_correct"].apply(to_bool)

    # auto correctness is from 'correct' column
    def auto_to_bool(x):
        s = str(x).strip().lower()
        return s in ["true", "1", "yes", "y"]

    df["auto_correct_bool"] = df["correct"].apply(auto_to_bool)

    overstated = (df["auto_correct_bool"] == True) & (df["human_correct_bool"] == False)
    understated = (df["auto_correct_bool"] == False) & (df["human_correct_bool"] == True)

    lines = []
    lines.append("# Manual Audit Summary\n")
    lines.append(f"Audited rows: {len(df)}\n")
    lines.append(f"Auto correct (in audited sample): {df['auto_correct_bool'].mean():.3f}\n")
    lines.append(f"Human correct (in audited sample): {df['human_correct_bool'].mean():.3f}\n")
    lines.append(f"Overstated cases (auto=True, human=False): {overstated.sum()}\n")
    lines.append(f"Understated cases (auto=False, human=True): {understated.sum()}\n\n")

    if overstated.any():
        lines.append("## Examples where automated metrics overstated performance\n")
        for _, r in df[overstated].head(5).iterrows():
            lines.append(f"- {r['id']}: expected='{r['expected_answer']}' | predicted='{r['predicted_answer']}' | notes='{r.get('notes','')}'")

    Path(OUT_PATH).write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote audit summary to {OUT_PATH}")

if __name__ == "__main__":
    main()
