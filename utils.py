import re

def extract_bib_field(entry_text: str, field_name: str) -> str:
    pattern = rf"{field_name}\s*=\s*[\{{\"](?P<val>.*?)[\}}\"][\s,]*$"
    m = re.search(pattern, entry_text, flags=re.IGNORECASE | re.DOTALL | re.MULTILINE)
    if not m:
        return ""
    value = m.group("val")
    value = re.sub(r"\s+", " ", value)
    return value.strip()

def getStudies(text):
    return [e for e in re.split(r"\n(?=@)", text) if e.strip().startswith("@")]