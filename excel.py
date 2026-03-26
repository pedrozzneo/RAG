import pandas as pd
from utils import getStudies, extract_bib_field

def save_llm_results_in_excel(ai, index, criterias, status):
    dataFrame = pd.read_excel("results/excelResults.xlsx")

    dataFrame.loc[index,f"{ai} criterias"]= criterias
    dataFrame.loc[index,f"{ai} status"]= status

    dataFrame.to_excel("results/excelResults.xlsx", index=False)
    
# save_llm_results_in_excel("GPT", 0, "IC4", "INCLUDED")

def save_db_source_in_excel(dbPath):
    with open(dbPath) as f: 
        text = f.read()

    studies = getStudies(text)

    for index, study in enumerate(studies):
        title = extract_bib_field(study, "title")
        dbCriterias = extract_bib_field(study, "criteria")
        dbStatus = extract_bib_field(study, "status")

        dataFrame = pd.read_excel("results/excelResults.xlsx")

        # Solve dtypes issues when the columns are empty
        dataFrame["title"] = dataFrame["title"].astype("object")
        dataFrame["db criterias"] = dataFrame["db criterias"].astype("object")
        dataFrame["db status"] = dataFrame["db status"].astype("object")

        dataFrame.loc[index, "title"] = title
        dataFrame.loc[index, "db criterias"] = dbCriterias
        dataFrame.loc[index, "db status"] = dbStatus

        dataFrame.to_excel("results/excelResults.xlsx", index=False)
        
save_db_source_in_excel("db_source/one.bib")