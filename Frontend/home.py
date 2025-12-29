import streamlit as st
import sys
import crewai
import pydantic
import asyncio
from dotenv import load_dotenv
load_dotenv()
import os
from crews import TrialCrew

folder_path = "output"
st.set_page_config(layout="wide")


def create_topic_list(input_string):
  topics = input_string.split(',')
  topics.sort() 
  topics = [j.strip().title() for j in topics]
  topic_list = []
  for topic in topics:
    # Strip leading/trailing whitespace from each topic
    topic_list.append({'topic': topic.strip().title()})
  return topics, topic_list

def run():
    
    async def main():
        # kickoff_for_each_async is async -> must be awaited
        async_results = await TrialCrew().crew().kickoff_for_each_async(
            inputs=input
        )

        # async_results is now a list -> you can iterate
        for i in async_results:
            print(i)

    asyncio.run(main())


st.title("Supplier Risk Procurement")
st.markdown("Input text or a csv file for the list of suppliers to start research!")

tabs = st.tabs(["Text", "File"])
with tabs[0]:
    text = st.text_input("Enter List of Suppliers")
with tabs[1]:
    files = st.file_uploader("Enter List of Suppliers")

topics, input = create_topic_list(text)


col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    start_research = st.button("🚀 Start Research", use_container_width=False, type="primary")
if start_research:
    run()


expander = st.expander("List of Files")
with expander:
    list = st.container(height=100)
    with list:
        st.write("**Suppliers Inputted:**")
        st.markdown(topics)
    crew_status = st.columns(3)
    with crew_status[0]:
        tile = st.container(height=350)
        tile.subheader("**Finance Files:**", anchor=False)
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".json") and file_name.startswith("finance_"):
                tile.write(file_name[8:-5])
    with crew_status[1]:
        tile = st.container(height=350)
        tile.subheader("**Credit Files:**", anchor=False)
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".json") and file_name.startswith("news_"):
                tile.write(file_name[5:-5])
    with crew_status[2]:
        tile = st.container(height=350)
        tile.subheader("**General Files:**", anchor=False)
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".json") and file_name.startswith("general_"):
                tile.write(file_name[8:-5])
