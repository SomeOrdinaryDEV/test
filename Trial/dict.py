import json
import os
import pandas as pd

folder_path = "output"   # path to your JSON files

fin_records = []
general_records = []
rep_records = []

# Load all JSON files into a list of dicts
for filename in os.listdir(folder_path):
    filepath = os.path.join(folder_path, filename)
    if filename.startswith("finance_"):
        # --- Finance files ---
        with open(filepath, "r") as f:
            data = json.load(f)
            # Drop unnecessary keys
            for col in ["key_insights", "red_flags", "strengths"]:
                data.pop(col, None)
            fin_records.append(data)
    
    elif filename.startswith("general_"):
         with open(filepath, "r") as f:
            data = json.load(f)
            # Drop unnecessary keys
            for col in ["primary_activities", "short_summary"]:
                data.pop(col, None)            
            general_records.append(data)
    elif filename.startswith("news_"):
         with open(filepath, "r") as f:
            data = json.load(f)
            # Drop unnecessary keys
            for col in ["key_insights", "red_flags", "strengths"]:
                data.pop(col, None)            
            rep_records.append(data)
# Create DataFrames
df_fin = pd.DataFrame(fin_records)
df_general = pd.DataFrame(general_records)
df_rep = pd.DataFrame(rep_records)

print(df_fin)
print("---")
print(df_general)
print("---")
print(df_rep)
