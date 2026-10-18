"""Context Sliding Window Shannon Entropy & Semantic Compactor.
100% Python Standard Library.
"""

import math

class ContextEntropyCompressor:
    """Computes per-turn Shannon information entropy to compress low-information conversational boilerplate while preserving critical directives."""

    @staticmethod
    def calculate_entropy(text: str) -> float:
        if not text:
            return 0.0
        freq = {}
        for ch in text:
            freq[ch] = freq.get(ch, 0) + 1
        n = len(text)
        return -sum((c / n) * math.log2(c / n) for c in freq.values())

    @classmethod
    def compress_context(cls, messages: list, max_tokens: int = 1000) -> dict:
        processed = []
        total_chars = 0
        pruned_count = 0

        for idx, msg in enumerate(messages):
            role = msg.get("role", "user")
            content = msg.get("content", "")
            is_critical = (role == "system" or idx == len(messages) - 1)

            if is_critical:
                processed.append(msg)
                total_chars += len(content)
            else:
                ent = cls.calculate_entropy(content)
                if ent < 2.5 and len(content) > 100:
                    summary = content[:60] + "... [low-entropy repetitive context pruned]"
                    processed.append({"role": role, "content": summary})
                    total_chars += len(summary)
                    pruned_count += 1
                else:
                    processed.append(msg)
                    total_chars += len(content)

        est_tokens = int(total_chars / 4)
        return {
            "original_messages": len(messages),
            "compressed_messages": len(processed),
            "low_entropy_turns_pruned": pruned_count,
            "estimated_token_count": est_tokens,
            "within_budget": est_tokens <= max_tokens,
            "messages": processed
        }
