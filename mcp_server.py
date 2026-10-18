"""MCP server for Context Sliding Window Shannon Entropy & Semantic Compactor."""
import sys
import json
from client import ContextEntropyCompressor

def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [{
                "name": "compress_context_entropy",
                "description": "Calculates Shannon entropy across conversation messages and prunes low-entropy turns",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "messages": {"type": "array"},
                        "max_tokens": {"type": "integer"}
                    },
                    "required": ["messages"]
                }
            }]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        if params.get("name") == "compress_context_entropy":
            msgs = params.get("arguments", {}).get("messages", [])
            max_t = int(params.get("arguments", {}).get("max_tokens", 1000))
            res = ContextEntropyCompressor.compress_context(msgs, max_t)
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
    return {"error": "Method not found"}

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_request(json.loads(line))))
            sys.stdout.flush()
