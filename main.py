import os
from LLMs.GPT import apply_first_criteria_with_llm
from excel import save_db_source_in_excel

def main():
    bib_path = os.path.join("db_source", "one.bib")
    save_db_source_in_excel(bib_path)
    # apply_first_criteria_with_llm(bib_path)    
main()
