import re

TOKEN_SPECS = [
    ("LOGIC_OP", r"\b(OR|AND|XOR)\b"),
    ("QUOTE", r"['\"]"),
    ("EQUALS", r"="),
    ("LITERAL", r"[a-zA-Z0-9_]+"),
]

def tokenize(text: str) -> list[str]:
    tokens = []
    text_upper = text.upper()
    
    # Kelimeler ve sembolleri ayıkla
    raw_tokens = re.findall(r"['\"]|\bOR\b|\bAND\b|\bXOR\b|=|[a-zA-Z0-9_]+", text_upper)
    
    for rt in raw_tokens:
        if rt in ("'", '"'):
            tokens.append("QUOTE")
        elif rt in ("OR", "AND", "XOR"):
            tokens.append("LOGIC_OP")
        elif rt == "=":
            tokens.append("EQUALS")
        elif rt.isalnum() or "_" in rt:
            tokens.append("LITERAL")
            
    return tokens
