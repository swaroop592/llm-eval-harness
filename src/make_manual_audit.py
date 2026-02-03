import pandas as pd

RESULTS_PATH = "results/results.csv"
AUDIT_PATH = "reports/manual_audit.csv"

def main():
    df = pd.read_csv(RESULTS_PATH)
    n = max(1, int(round(0.10 * len(df))))
    sample = df.sample(n=n, random_state=42).copy()

    sample["human_correct"] = ""
    sample["notes"] = ""
    sample.to_csv(AUDIT_PATH, index=False)
    print(f"Wrote {n} rows to {AUDIT_PATH}")

if __name__ == "__main__":
    main()
