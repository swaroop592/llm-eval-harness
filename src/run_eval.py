import argparse
import yaml
import pandas as pd

from src.loaders import load_documents, load_gold_qa
from src.providers.mock_provider import MockProvider
from src.scoring import is_correct
from src.metrics import compute_accuracy, accuracy_by_case_type, not_found_prf
from src.cost import estimate_cost
from src.report import write_summary


def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def get_provider(name: str):
    if name == "mock":
        return MockProvider()
    raise ValueError(f"Unknown provider: {name}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Path to YAML config")
    args = parser.parse_args()

    cfg = load_config(args.config)

    docs = load_documents(cfg["docs_dir"])
    qa = load_gold_qa(cfg["qa_path"])

    provider_name = cfg["provider"]
    provider = get_provider(provider_name)

    rows = []

    for item in qa:
        doc = docs[item["doc_id"]]
        prompt = f"{doc}\n\nQuestion: {item['question']}"

        output = provider.generate(prompt)

        correct = is_correct(output["answer"], item["expected_answer"])
        cost = estimate_cost(
            provider_name,
            output["prompt_tokens"],
            output["completion_tokens"],
        )

        rows.append({
            "id": item["id"],
            "doc_id": item["doc_id"],
            "case_type": item["case_type"],
            "expected_answer": item["expected_answer"],
            "predicted_answer": output["answer"],
            "correct": correct,
            "latency_ms": output["latency_ms"],
            "prompt_tokens": output["prompt_tokens"],
            "completion_tokens": output["completion_tokens"],
            "cost_usd": cost,
        })

    df = pd.DataFrame(rows)
    df.to_csv(cfg["results_path"], index=False)

    acc = compute_accuracy(df)
    acc_cases = accuracy_by_case_type(df)
    prf = not_found_prf(df)

    summary = f"""LLM Evaluation Summary ({provider_name})

Config: {args.config}
Total questions: {len(df)}
Overall accuracy: {acc:.3f}

Accuracy by case type:
"""
    for k, v in acc_cases.items():
        summary += f"- {k}: {v:.3f}\n"
    summary += f"\nNOT_FOUND detection (positive class = NOT_FOUND):\n"
    summary += f"- precision: {prf['precision']:.3f}\n"
    summary += f"- recall: {prf['recall']:.3f}\n"
    summary += f"- f1: {prf['f1']:.3f}\n"
    summary += f"- tp/fp/fn: {prf['tp']}/{prf['fp']}/{prf['fn']}\n"


    write_summary(cfg["summary_path"], summary)

    print("Evaluation complete.")
    print(summary)

if __name__ == "__main__":
    main()
