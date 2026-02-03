import pandas as pd

def compute_accuracy(df: pd.DataFrame):
    return df["correct"].mean()

def accuracy_by_case_type(df: pd.DataFrame):
    return df.groupby("case_type")["correct"].mean().to_dict()

def not_found_prf(df: pd.DataFrame):
    """
    Treat NOT_FOUND as the positive class for detection.
    """
    expected_nf = df["expected_answer"].astype(str).str.strip().str.upper().eq("NOT_FOUND")
    predicted_nf = df["predicted_answer"].astype(str).str.strip().str.upper().eq("NOT_FOUND")

    tp = (expected_nf & predicted_nf).sum()
    fp = (~expected_nf & predicted_nf).sum()
    fn = (expected_nf & ~predicted_nf).sum()

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0

    return {
        "tp": int(tp),
        "fp": int(fp),
        "fn": int(fn),
        "precision": float(precision),
        "recall": float(recall),
        "f1": float(f1),
    }

def not_found_confusion(df: pd.DataFrame):
    expected_nf = df["expected_answer"].astype(str).str.strip().str.upper().eq("NOT_FOUND")
    predicted_nf = df["predicted_answer"].astype(str).str.strip().str.upper().eq("NOT_FOUND")

    tp = int((expected_nf & predicted_nf).sum())
    fp = int((~expected_nf & predicted_nf).sum())
    fn = int((expected_nf & ~predicted_nf).sum())
    tn = int((~expected_nf & ~predicted_nf).sum())

    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn}
