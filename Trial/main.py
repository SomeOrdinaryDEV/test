import sys
from crew import TrialCrew
import crewai
import pydantic
import asyncio
import streamlit as st
import json
def create_topic_list(input_string):
  topics = input_string.split(',')
  topics.sort() 
  topics = [j.strip().title() for j in topics]
  topic_list = []
  for topic in topics:
    # Strip leading/trailing whitespace from each topic
    topic_list.append({'topic': topic.strip().title()})
  return topics, topic_list

# Example usage:
input_string = "Taj Hospitality"

topics, input = create_topic_list(input_string)

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

run()

"""
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    start_research = st.button("🚀 Start Research", use_container_width=False, type="primary")

if start_research:
    with st.status("🤖 Researching...", expanded=True) as status:
      run()
"""