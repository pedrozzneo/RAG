import os
import json
from openai import OpenAI
from prompts import build_prompt1, build_prompt2, build_prompt3
from utils import extract_bib_field, getStudies
from excel import save_llm_results_in_excel, compare_ai_accuracy_status

def apply_first_criteria_with_llm(selected_bib_path):
    with open(selected_bib_path, "r", encoding="utf-8") as f:
        text = f.read()

    studies = getStudies(text)
    studiesLen = len(studies)
    print(f"\nStarting LLM evaluation for {studiesLen} studies...")

    for index, study in enumerate(studies):
        title = extract_bib_field(study, "title")
        abstract = extract_bib_field(study, "abstract")

        print(f"({index+1}/{studiesLen}) -> Evaluating: {title[:80]} ")
    
        for promptNumber in range(3):
            if(promptNumber == 0):
                prompt = build_prompt1(title, abstract)
            elif(promptNumber == 1):
                prompt = build_prompt2(title, abstract)
            elif(promptNumber == 2):
                prompt = build_prompt3(title, abstract)
            
            client = OpenAI()
            response = client.responses.create(
                model="gpt-5.4",
                input=prompt
            )

            responseDict = json.loads(response.output_text)

            llmCriterias = ", ".join(responseDict["llmCriterias"])
            llmStatus = responseDict["llmStatus"]

            save_llm_results_in_excel("GPT", promptNumber, index, llmCriterias, llmStatus)

    
    for promptNumber in range(3):
        print(f"Comparing GPT accuracy status for prompt {promptNumber+1}...")
        compare_ai_accuracy_status("GPT", promptNumber)
