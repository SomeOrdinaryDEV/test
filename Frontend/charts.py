import streamlit as st
import json
import os
import pandas as pd

st.set_page_config(layout="wide")

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

st.title("Charts")
st.divider()


st.subheader("Financial Risk")
st.bar_chart(df_fin, x="company", y="score", stack=True, x_label="Company", y_label="Financial Risk", color="company")
expander = st.expander("Show Financial details")
with expander:       
    st.subheader("Revenue (past year, in $USD)")
    st.bar_chart(df_fin, x="company", y="revenue", stack=True, x_label="Revenue", y_label="Company", color="company",  horizontal=True)

    st.subheader("Growth Rate (past year, in %)")
    st.bar_chart(df_fin, x="company", y="growth_rate", stack=True, x_label="Previous Year Growth Rate", y_label="Company", color="#6696fc", horizontal=True)
    
    st.subheader("Liquidity (in $USD)")
    st.bar_chart(df_fin, x="company", y="liquidity", stack=True, x_label="Liquidity (in $USD)", y_label="Company", color="company",  horizontal=True)

    st.subheader("Profit Margins (in %)")
    st.bar_chart(df_fin, x="company", y="profit_margins", stack=True, x_label="Profit Margin (in %)", y_label="Company", color="company",  horizontal=True)


st.subheader("Reputational Risk")
st.bar_chart(df_rep, x="company", y="score", stack=True, x_label="Company", y_label="Financial Risk", color="company")
expander = st.expander("Show Reputational details")
with expander:       
    st.subheader("Environmental Ratings (from 1-100)")
    st.bar_chart(df_rep, x="company", y="environmental_rating", stack=True, x_label="Environmental Rating", y_label="Company", color="company",  horizontal=True)

    st.subheader("Product Quality Ratings (from 1-100)")
    st.bar_chart(df_rep, x="company", y="product_quality_rating", stack=True, x_label="Product Quality Ratings", y_label="Company", color="#6696fc", horizontal=True)

    st.subheader("Profit Margins (in %)")
    st.bar_chart(df_fin, x="company", y="profit_margins", stack=True, x_label="Profit Margin (in %)", y_label="Company", color="company",  horizontal=True)

