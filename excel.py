import pandas as pd

def save_llm_results_in_excel(ai, index, criterias, status):
    dataFrame = pd.read_excel("results/excelResults.xlsx")

    dataFrame.loc[index,f"{ai} criterias"]= criterias
    dataFrame.loc[index,f"{ai} status"]= status

    dataFrame.to_excel("results/excelResults.xlsx", index=False)
    
# save_llm_results_in_excel("GPT", 0, "IC4", "INCLUDED")

def save_db_source_in_excel(index, title, dbCriterias, dbStatus):
    dataFrame = pd.read_excel("results/excelResults.xlsx")

    dataFrame.loc[index, "title"] = title
    dataFrame.loc[index, "db criterias"] = dbCriterias
    dataFrame.loc[index, "db status"] = dbStatus

    dataFrame.to_excel("results/excelResults.xlsx", index=False)

for i in range(5):
    save_db_source_in_excel(i, "test", "IC2", "INCLUDED")