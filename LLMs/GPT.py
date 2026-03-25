import re
import os
from utils import extract_bib_field
from openai import OpenAI
from prompts import build_prompt1

def apply_first_criteria_with_llm(selected_bib_path):
    out_dir = os.path.join("results", "GPT", "first_criteria.txt")

    with open(selected_bib_path, "r", encoding="utf-8") as f:
        text = f.read()

    print(text)

    raw_entries = [e for e in re.split(r"\n(?=@)", text) if e.strip().startswith("@")]
    total = len(raw_entries)
    print(f"\nStarting LLM evaluation for {total} studies...")

    with open(out_dir, "w", encoding="utf-8") as out_dir:
        for idx, entry in enumerate(raw_entries, start=1):
            entry_strip = entry.strip()

            title = extract_bib_field(entry_strip, "title")
            abstract = extract_bib_field(entry_strip, "abstract")

            print(f"[FirstCriteria] ({idx}/{total}) evaluating: {title[:80]}")
        
            prompt = build_prompt1(title, abstract)

            client = OpenAI()
            response = client.responses.create(
                model="gpt-5.4",
                input=prompt
            )

            print(response.output_text)

            out_dir.write(response.output_text)
            out_dir.write("\n\n")

    return out_dir

