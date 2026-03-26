import pandas as pd

def save_in_excel_results(ai, index, criterias, status):
    dataFrame = pd.read_excel("results/excelResults.xlsx")

    dataFrame.loc[index,f"{ai} criterias"]= criterias
    dataFrame.loc[index,f"{ai} status"]= status

    dataFrame.to_excel("results/excelResults.xlsx", index=False)
    
save_in_excel_results("GPT", 0, "IC2", "INCLUDED")