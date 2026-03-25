import re
import os
from utils import extract_bib_field
from openai import OpenAI

def apply_first_criteria_with_llm(selected_bib_path):

    out_dir = os.path.join("results", "first_criteria_application")
    out_filename = "first_criteria.bib"
    model = "llama3.2:1b"

    with open(selected_bib_path, "r", encoding="utf-8") as f:
        text = f.read()

    print(text)

    raw_entries = [e for e in re.split(r"\n(?=@)", text) if e.strip().startswith("@")]
    total = len(raw_entries)
    print(f"\nStarting LLM evaluation for {total} studies...")

    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, out_filename)

    def _build_prompt(title: str, abstract: str) -> str:
        return (
            "You are assisting in a systematic literature review about service-oriented robotic systems.\n"
            "Your task is to return a list of checked inclusion criteria, a list of checked exclusion criteria and the llmStatus like this: included = [LIST OF INCLUDED CRITERIAS], excluded = [LIST OF EXCLUDED CRITERIAS], llmStatus = [LLMSTATUS]\n"

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

            "you will put all the identified inclusion criterias in a list called included like this: included = ['IC1', 'IC2']\n"
            "you will put all the identified exclusion criterias in a list called excluded like this: excluded = ['EC1', 'EC4']\n" 
            "analysing those 2 lists YOU created (included and excluded) you will determine the llm status, following these rules:\n"
            "- if the included list is NOT empty and the excluded list is empty, the llm status will be INCLUDED\n"
            "- if the excluded list is NOT empty and the included list is empty, the llm status will be EXCLUDED\n"
            "- Any other situation, meaning the llm status is NOT INCLUDED and NOT EXCLUDED, the llm status be marked as PENDING\n"

            "IMPORTANT:\n"
            "- If you are unsure about a criteria, DO NOT include its code in the output.\n"
            "- Do not try to infer details that are not suggested by the title/abstract.\n\n"

            "Now analyze this study:\n\n"
            f"TITLE: {title.strip()}\n"
            f"ABSTRACT: {abstract.strip()}\n"
        )

    with open(out_path, "w", encoding="utf-8") as out_f:
        for idx, entry in enumerate(raw_entries, start=1):
            entry_strip = entry.strip()

            title = extract_bib_field(entry_strip, "title")
            abstract = extract_bib_field(entry_strip, "abstract")

            print(f"[FirstCriteria] ({idx}/{total}) evaluating: {title[:80]}")
        
            prompt = _build_prompt(title, abstract)
            # response = ask_ollama(prompt, model=model)

            client = OpenAI()
            response = client.responses.create(
                model="gpt-5.4",
                input=prompt
            )

            print(response.output_text)

            # out_f.write(response)
            # out_f.write("\n\n")

    return out_path

