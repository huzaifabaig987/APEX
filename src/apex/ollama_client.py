"""Connect APEX to a local Ollama language model."""

import json
from urllib.request import Request, urlopen


OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "qwen2.5:3b"


def generate(prompt: str, model: str = DEFAULT_MODEL) -> str:
    """Send a prompt to Ollama and return the model response."""
    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False,
    }).encode("utf-8")

    request = Request(
        OLLAMA_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urlopen(request, timeout=180) as response:
        result = json.loads(response.read().decode("utf-8"))

    return result["response"].strip()


if __name__ == "__main__":
    print("Testing APEX -> Python -> Ollama -> Qwen2.5 3B")
    answer = generate("Reply with exactly: APEX Python connection works.")
    print(f"Model response: {answer}")
    print("Connection test completed.")
