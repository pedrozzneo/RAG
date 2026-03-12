import json
import re
import os
import requests
from bibtex_utils import extract_bib_field


def ask_ollama(prompt: str, model: str = "llama3.2:1b") -> str:
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }

    resp = requests.post(url, json=payload, timeout=60)

    if resp.status_code != 200:
        return ""

    data = resp.json()
    return data.get("response", "")


def apply_first_criteria_with_llm(
    selected_bib_path: str = os.path.join("process", "search_string", "selected.bib"),
    out_dir: str = os.path.join("process", "first_criteria_application"),
    out_filename: str = "first_criteria.bib",
    model: str = "llama3.2:1b",
) -> str:

    with open(selected_bib_path, "r", encoding="utf-8") as f:
        text = f.read()

    raw_entries = [e for e in re.split(r"\n(?=@)", text) if e.strip().startswith("@")]
    total = len(raw_entries)
    print(f"\n[FirstCriteria] Starting LLM evaluation for {total} studies...")

    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, out_filename)

    def _build_prompt(title: str, abstract: str) -> str:
        return (
            "You are assisting in a systematic literature review about service-oriented robotic systems.\n"
            "Your task is to decide, based ONLY on the TITLE and ABSTRACT, which of the following criteria apply.\n\n"
            "Inclusion criteria:\n"
            "IC1: The primary study proposes or reports on the design and development of a service-oriented robotic system.\n"
            "IC2: The primary study proposes or reports on a new technology for developing service-oriented robotic systems.\n"
            "IC3: The primary study proposes or reports on a process, method, technique, reference architecture or any software engineering guideline that supports either the design or the development of service-oriented robotic systems.\n\n"
            "Exclusion criteria:\n"
            "EC1: The primary study reports on the development of a robotic systems without using SOA.\n"
            "EC2: The primary study presents contributions in areas other than Robotics.\n"
            "EC3: The primary study does not report on the design or development of service-oriented robotic system.\n"
            "EC4: The study is a previous version of a more complete study about the same research.\n"
            "EC5: The primary study is a table of contents, short course description, tutorial, copyright form or summary of an event.\n\n"
            "IMPORTANT:\n"
            "- Base your decision ONLY on the TITLE and ABSTRACT below.\n"
            "- Decide which IC* and EC* codes from the lists above clearly apply.\n"
            "- If you are unsure about a criterion, DO NOT include its code in the output.\n"
            "- Do not try to infer details that are not suggested by the title/abstract.\n\n"
            "Return your answer ONLY as a compact JSON object with this exact structure (no explanations, no extra keys, no comments):\n"
            '{\"IC\": [\"IC1\", \"IC3\"], \"EC\": [\"EC3\"]}\n\n'
            "Now analyze this study:\n\n"
            f"TITLE: {title.strip()}\n"
            f"ABSTRACT: {abstract.strip()}\n"
        )

    def _extract_llm_decision(title: str, abstract: str):
        prompt = _build_prompt(title, abstract)
        raw = ask_ollama(prompt, model=model)
        ic_list = []
        ec_list = []
        try:
            data = json.loads(raw)
            raw_ic = [c for c in data.get("IC", []) if isinstance(c, str)]
            raw_ec = [c for c in data.get("EC", []) if isinstance(c, str)]
        except Exception:
            # Fallback: try to detect codes with regex if not valid JSON
            raw_ic = re.findall(r"\bIC[1-3]\b", raw)
            raw_ec = re.findall(r"\bEC[1-5]\b", raw)

        # Keep only valid IC*/EC* codes, normalize and deduplicate
        ic_list = sorted({c for c in raw_ic if re.fullmatch(r"IC[1-3]", c)})
        ec_list = sorted({c for c in raw_ec if re.fullmatch(r"EC[1-5]", c)})

        # Build final criteria and status
        all_codes = ic_list + ec_list
        if ec_list:
            status = "EXCLUDED"
        elif ic_list:
            status = "INCLUDED"
        else:
            status = "UNDECIDED"

        # If nothing applies, leave criteria empty and rely on llmStatus=UNDECIDED
        criteria_str = ", ".join(all_codes) if all_codes else ""
        return criteria_str, status

    with open(out_path, "w", encoding="utf-8") as out_f:
        for idx, entry in enumerate(raw_entries, start=1):
            entry_strip = entry.strip()

            title = extract_bib_field(entry_strip, "title")
            abstract = extract_bib_field(entry_strip, "abstract")

            print(f"[FirstCriteria] ({idx}/{total}) evaluating: {title[:80]}")
            criteria_str, status = _extract_llm_decision(title, abstract)
            print(f"[FirstCriteria] --> llmCriteria={criteria_str} | llmStatus={status}")

            # Remove any previous llm* fields if present
            cleaned = re.sub(
                r"\n\s*llmCriteria\s*=\s*\{.*?\},?", "", entry_strip, flags=re.IGNORECASE | re.DOTALL
            )
            cleaned = re.sub(
                r"\n\s*llmStatus\s*=\s*\{.*?\},?", "", cleaned, flags=re.IGNORECASE | re.DOTALL
            )

            # Insert new llmCriteria and llmStatus before the final closing brace
            closing_idx = cleaned.rfind("}")
            if closing_idx == -1:
                new_entry = (
                    cleaned
                    + f"\n  llmCriteria = {{{criteria_str}}},\n  llmStatus = {{{status}}}\n"
                )
            else:
                prefix = cleaned[:closing_idx].rstrip()
                new_entry = (
                    prefix
                    + f"\n  llmCriteria = {{{criteria_str}}},\n  llmStatus = {{{status}}}\n"
                    + "}"
                )

            out_f.write(new_entry)
            out_f.write("\n\n")

    print(f"[FirstCriteria] Finished. Output: {out_path}")
    return out_path

