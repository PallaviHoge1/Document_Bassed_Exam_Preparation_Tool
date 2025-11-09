import os, re, json

BACKEND = os.getenv("LLM_BACKEND", "ollama").lower()
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")

INSTR = (
    "You create multiple-choice questions (MCQs) for exam prep based on the summary.\n"
    "- Create EXACTLY {n} questions.\n"
    "- Each question MUST have four options (a,b,c,d) and one correct answer (a/b/c/d).\n"
    "- Respond with STRICT JSON ONLY.\n"
    "- Output MUST be a single JSON array of objects with fields:\n"
    "  question: string,\n"
    "  options: {{a: string, b: string, c: string, d: string}},\n"
    "  answer: one of 'a','b','c','d'.\n"
    "DO NOT include any preface, explanation, markdown, or code fences.\n"
    "Wrap ONLY the JSON array between the markers:\n"
    "<BEGIN_JSON>\n"
    "[ ... ]\n"
    "<END_JSON>"
)

_JSON_BLOCK_RE = re.compile(
    r"<BEGIN_JSON>\s*(\[\s*[\s\S]*?\s*\])\s*<END_JSON>",
    re.IGNORECASE,
)

def _extract_json_block(text: str) -> str:
    m = _JSON_BLOCK_RE.search(text)
    block = None
    if m:
        block = m.group(1)
    else:
        start, end = text.find("["), text.rfind("]")
        if start != -1 and end != -1 and end > start:
            block = text[start:end+1]
    if block is None:
        raise ValueError("No JSON array found in model output")

    # light repairs: trailing commas before ']' or '}'
    block = re.sub(r",\s*(\]|\})", r"\1", block)
    return block

def _parse_json_maybe(text: str):
    block = _extract_json_block(text)
    try:
        return json.loads(block)
    except json.JSONDecodeError as e:
        preview = block[:300].replace("\n", " ")
        raise ValueError(f"Malformed JSON from model. Preview: {preview}") from e

def _normalize_options(options):
    """
    Accepts:
      - dict with any key case/ordering
      - list/tuple of 4 strings
    Returns dict {a,b,c,d} -> str, or {} if invalid.
    """
    if isinstance(options, dict):
        # lowercase string keys
        norm = {}
        for k, v in options.items():
            kk = str(k).strip().lower()
            norm[kk] = (v or "").strip()
        # if keys are like "option_a" or "A", try to map
        candidates = {}
        for key in ("a","b","c","d"):
            if key in norm:
                candidates[key] = norm[key]
        # if still missing, try to pull from first four values in order
        if len(candidates) != 4:
            vals = [str(v).strip() for v in options.values()]
            if len(vals) >= 4:
                candidates = {k: vals[i] for i, k in enumerate(("a","b","c","d"))}
        return candidates if set(candidates.keys()) == {"a","b","c","d"} else {}

    if isinstance(options, (list, tuple)) and len(options) >= 4:
        return {k: str(options[i]).strip() for i, k in enumerate(("a","b","c","d"))}

    return {}

def _normalize_answer(answer, options_dict):
    """
    Accepts letter or full option text. Returns 'a'|'b'|'c'|'d' if resolvable, else ''.
    """
    if not options_dict:
        return ""
    if isinstance(answer, str):
        ans = answer.strip().lower()
        if ans in {"a","b","c","d"}:
            return ans
        # try match by text
        for k, v in options_dict.items():
            if v.strip().lower() == ans:
                return k
    return ""

def _quiz_with_ollama(summary: str, n: int):
    from ollama import Client
    client = Client()

    INSTR_TEXT = INSTR.format(n=n)

    prompt = (
        f"{INSTR_TEXT}\n\n"
        f"Summary:\n{summary}\n\n"
        "Remember: ONLY produce the JSON array between <BEGIN_JSON> and <END_JSON>."
    )

    resp = client.chat(
        model=OLLAMA_MODEL,
        messages=[{"role":"user","content": prompt}],
        options={
            "temperature": 0.1,
            "stop": ["<END_JSON>", "</END_JSON>"],
            "num_predict": 800
        },
    )
    content = resp["message"]["content"].strip()
    raw_items = _parse_json_maybe(content)

    cleaned = []
    for item in raw_items:
        question = (item.get("question") or "").strip()
        options_raw = item.get("options")
        answer_raw = item.get("answer")

        options = _normalize_options(options_raw)
        print(options)
        if not options or not question:
            continue

        answer = _normalize_answer(answer_raw, options)
        if answer not in {"a","b","c","d"}:
            # fallback: default to 'a' to prevent crashes, but skip if empty option
            answer = "a" if options.get("a","").strip() else ""

        if answer:
            cleaned.append({
                "question": question,
                "options": options,
                "answer": answer
            })

    if not cleaned:
        raise ValueError("Parsed JSON but no valid MCQs after normalization/validation.")
    return cleaned

def generate_mcqs(summary: str, num_questions: int = 5):
    if BACKEND == "ollama":
        return _quiz_with_ollama(summary, num_questions)
    raise RuntimeError(f"Unsupported LLM_BACKEND={BACKEND} for quiz generation")
