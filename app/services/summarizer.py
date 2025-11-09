import os
import json

BACKEND = os.getenv("LLM_BACKEND", "ollama").lower()
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")

def _summarize_with_ollama(snippet: str) -> str:
    from ollama import Client
    client = Client()
    prompt = (
        "Summarize the following content into 5–10 short, factual bullet points for quick study. "
        "Avoid fluff or repetition. Return only bullet points.\n\n"
        f"{snippet}"
    )
    resp = client.chat(model=OLLAMA_MODEL, messages=[{"role": "user", "content": prompt}])
    return resp["message"]["content"].strip()

def summarize_text(content: str, max_chars: int = 12000) -> str:
    snippet = content[:max_chars]
    if BACKEND == "ollama":
        return _summarize_with_ollama(snippet)

    # Fallbacks if you ever switch BACKEND
    if BACKEND == "openai":
        from openai import OpenAI
        client = OpenAI()
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        r = client.chat.completions.create(
            model=model, messages=[{"role": "user", "content": 
                "Summarize into 5–10 bullet points:\n\n" + snippet}],
            temperature=0.2, max_tokens=600
        )
        return r.choices[0].message.content.strip()

    if BACKEND == "hf":
        from huggingface_hub import InferenceClient
        model = os.getenv("HUGGINGFACE_MODEL", "HuggingFaceH4/zephyr-7b-beta")
        token = os.getenv("HUGGINGFACE_API_KEY") or None
        client = InferenceClient(model=model, token=token)
        r = client.chat.completions.create(
            model=model, messages=[{"role":"user","content":
                "Summarize into 5–10 bullet points:\n\n" + snippet}],
            temperature=0.2, max_tokens=600
        )
        return r.choices[0].message["content"].strip()

    raise RuntimeError(f"Unsupported LLM_BACKEND={BACKEND}")
