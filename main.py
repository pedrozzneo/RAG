import os
from LLMs.GPT import apply_first_criteria_with_llm

def main():
    bib_path = os.path.join("db_source", "one.bib")
    apply_first_criteria_with_llm(bib_path)    
main()
