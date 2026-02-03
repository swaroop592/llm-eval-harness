PRICING = {
    "mock": {
        "prompt_per_1k": 0.0,
        "completion_per_1k": 0.0,
    }
}

def estimate_cost(provider: str, prompt_tokens: int, completion_tokens: int):
    pricing = PRICING.get(provider)
    if pricing is None:
        return 0.0

    cost = (
        prompt_tokens / 1000 * pricing["prompt_per_1k"]
        + completion_tokens / 1000 * pricing["completion_per_1k"]
    )
    return cost
