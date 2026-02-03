import json
from pathlib import Path

def load_documents(docs_dir: str):
    """
    Load documents from data/docs into a dict keyed by doc_id.
    """
    docs = {}
    for path in Path(docs_dir).glob("*.txt"):
        doc_id = path.stem
        docs[doc_id] = path.read_text(encoding="utf-8")
    return docs


def load_gold_qa(path: str):
    """
    Load gold QA dataset from JSONL.
    """
    qa = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            qa.append(json.loads(line))
    return qa
