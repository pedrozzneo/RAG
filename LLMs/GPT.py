import re
import os
from utils import extract_bib_field, getStudies
from openai import OpenAI
from prompts import build_prompt1

def apply_first_criteria_with_llm(selected_bib_path):
    result_dir = os.path.join("results", "GPT", "first_criteria.txt")

    with open(selected_bib_path, "r", encoding="utf-8") as f:
        text = f.read()

    studies = getStudies(text)
    studiesLen = len(studies)
    print(f"\nStarting LLM evaluation for {studiesLen} studies...")

    with open(result_dir, "w", encoding="utf-8") as result_dir:
        for index, study in enumerate(studies):
            title = extract_bib_field(study, "title")
            abstract = extract_bib_field(study, "abstract")

            print(f"({index+1}/{studiesLen}) -> Evaluating: {title[:80]} ")
        
            prompt = build_prompt1(title, abstract)

            client = OpenAI()
            response = client.responses.create(
                model="gpt-5.4",
                input=prompt
            )

            print(response.output_text)

            result_dir.write(response.output_text)
            result_dir.write("\n\n")
    return result_dir

