import os
import re
from urllib.parse import quote
import xml.etree.ElementTree as ET
from ollama import apply_first_criteria_with_llm
from bibtex_utils import extract_bib_field


def apply_search_string(bib_path: str):
    with open(bib_path, "r", encoding="latin-1") as f:
        text = f.read()

    # Split into entries – each starting with a line beginning with '@'
    raw_entries = re.split(r"\n(?=@)", text)

    service_terms = [
        "service oriented",
        "service-oriented",
        "service based",
        "service-based",
        "service orientation",
        "soa",
    ]
    robot_terms = [
        "robot",
        "robotic",
        "humanoid",
    ]
    selected = []

    for entry in raw_entries:
        entry_strip = entry.strip()
        if not entry_strip.startswith("@"):
            continue

        # BibTeX key: @TYPE{KEY,
        m_key = re.match(r"@\w+\s*{\s*([^,]+),", entry_strip)
        key = m_key.group(1).strip() if m_key else ""

        title = extract_bib_field(entry_strip, "title")
        abstract = extract_bib_field(entry_strip, "abstract")
        keywords = extract_bib_field(entry_strip, "keywords") or extract_bib_field(
            entry_strip, "keyword"
        )

        haystack = " ".join([title, abstract, keywords]).lower()

        if not haystack.strip():
            continue

        has_service = any(term in haystack for term in service_terms)
        has_robot = any(term in haystack for term in robot_terms)

        if has_service and has_robot:
            selected.append(
                {
                    "key": key,
                    "title": title,
                    "abstract": abstract,
                    "keywords": keywords,
                    "raw_entry": entry_strip,
                }
            )
    return selected


def save_systematic_review_selection(selected_entries,base_dir: str = "process",search_folder: str = "search_string",filename: str = "selected.bib"):
    out_dir = os.path.join(base_dir, search_folder)
    os.makedirs(out_dir, exist_ok=True)

    out_path = os.path.join(out_dir, filename)
    with open(out_path, "w", encoding="utf-8") as f:
        for entry in selected_entries:
            f.write(entry["raw_entry"])
            f.write("\n\n")

    print(f"Saved {len(selected_entries)} selected studies to: {out_path}")
    return out_path

def main():
    # 1) Filter (first process: search_string)
    bib_path = os.path.join("db_source", "test.bib")
    selected = apply_search_string(bib_path)
    search_string_path = save_systematic_review_selection(selected)

    print(f"\nFirst process (search_string) completed.")
    print(f"Number of selected studies: {len(selected)}")

    # 2) Apply first criteria with LLM on the filtered set
    first_criteria_path = apply_first_criteria_with_llm(
        selected_bib_path=search_string_path
    )
    print(f"First criteria application file: {first_criteria_path}")
if __name__ == "__main__":
    main()
