import streamlit as st

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
st.session_state.df_fin = pd.DataFrame(fin_records)
st.session_state.df_gen = pd.DataFrame(general_records)
st.session_state.df_rep = pd.DataFrame(rep_records)

df_fin = st.session_state.df_fin
df_gen = st.session_state.df_gen
df_rep = st.session_state.df_rep

st.header("Data")
st.subheader("Financial Data Findings", divider=True)
st.dataframe(df_fin)
st.subheader("Reputational Data Findings", divider=True)
st.dataframe(df_rep)
st.subheader("General Findings", divider=True)
st.dataframe(df_gen)
