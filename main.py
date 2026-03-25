import os
from LLMs.GPT import apply_first_criteria_with_llm

def main():
    bib_path = os.path.join("db_source", "one.bib")
    first_criteria_path = apply_first_criteria_with_llm(bib_path)
    print(f"First criteria application file: {first_criteria_path}")
if __name__ == "__main__":
    main()
