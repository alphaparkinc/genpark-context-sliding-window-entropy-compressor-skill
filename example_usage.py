"""Example usage for Context Sliding Window Shannon Entropy & Semantic Compactor."""
from client import ContextEntropyCompressor

if __name__ == "__main__":
    msgs = [
        {"role": "system", "content": "You are a specialized code optimization assistant."},
        {"role": "user", "content": "repeat repeat repeat repeat repeat repeat repeat repeat repeat repeat repeat repeat repeat repeat"},
        {"role": "assistant", "content": "Refactored the AST parsing module for zero external dependencies."}
    ]
    res = ContextEntropyCompressor.compress_context(msgs)
    print("Pruned Turns:", res["low_entropy_turns_pruned"])
    print("Within Budget:", res["within_budget"])
