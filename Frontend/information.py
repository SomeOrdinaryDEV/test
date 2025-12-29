import streamlit as st
import os
import json
folder_path = "output"

st.header("Types of Information")
display_type = st.segmented_control("", ["General", "Financial", "Reputational"], default="General")

if display_type == "General":
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".json") and file_name.startswith("general_"):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)  
            # Display it in Streamlit
            st.header(data["legal_name"], divider=True)
            st.markdown(data["short_summary"],width="stretch")
            st.write("**Primary Activities:** " + ", ".join(data["primary_activities"]))        
            st.write("**Number of countries operated in:** ", data["locations_of_operation"])
elif display_type == "Financial":
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".json") and file_name.startswith("finance_"):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)  
            # Display it in Streamlit
            st.header(data["company"], divider=True)
            st.markdown(data["key_insights"],width="stretch")
            expander = st.expander("Pros and Cons")
            with expander:
                pros_and_cons = st.columns(2)
                with pros_and_cons[0]:
                    tile = st.container(height=300)
                    tile.subheader("Red Flags", anchor=False) 
                    for flag in data["red_flags"]: tile.write(f"- {flag}")
                with pros_and_cons[1]:
                    tile = st.container(height=300)
                    tile.subheader("Strengths", anchor=False) 
                    for flag in data["strengths"]: tile.write(f"- {flag}")
elif display_type == "Reputational":
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".json") and file_name.startswith("news_"):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)  
            # Display it in Streamlit
            st.header(data["company"], divider=True)
            st.markdown(data["key_insights"],width="stretch")
            expander = st.expander("Pros and Cons")
            with expander:
                pros_and_cons = st.columns(2)
                with pros_and_cons[0]:
                    tile = st.container(height=300)
                    tile.subheader("Red Flags", anchor=False) 
                    for flag in data["red_flags"]: tile.write(f"- {flag}")
                with pros_and_cons[1]:
                    tile = st.container(height=300)
                    tile.subheader("Strengths", anchor=False) 
                    for flag in data["strengths"]: tile.write(f"- {flag}")    
