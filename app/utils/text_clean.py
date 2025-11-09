import re

def normalize_whitespace(text: str) -> str:
    text = text.replace("\u00ad", "")  # soft hyphen
    text = re.sub(r"-\n", "", text)    # end-line hyphenation
    text = re.sub(r"\r\n|\r|\n", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
