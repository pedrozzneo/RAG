import os
import json
from openai import OpenAI
from prompts import build_prompt1
from utils import extract_bib_field, getStudies
from excel import save_llm_results_in_excel


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

            responseDict = json.loads(response.output_text)
            
            llmCriterias = ", ".join(responseDict["llmCriterias"])
            llmStatus = responseDict["llmStatus"]

            # Isolated save 
            result_dir.write(response.output_text)
            result_dir.write("\n\n")

            # Save in excel as well to compare
            save_llm_results_in_excel("GPT", index, llmCriterias, llmStatus)
    return result_dir

