from crewai import Agent, Task, LLM, Crew, Process
from crewai_tools import TXTSearchTool, SerperDevTool
import os
from dotenv import load_dotenv
import streamlit as st
from google import genai
import json

load_dotenv()
path = "output"
tool2 = SerperDevTool()

llm = LLM(model="gemini/gemini-2.5-flash",
          temperature=0.5,)

def merge_txt(folder):
    text = ""
    for file_name in os.listdir(folder):
        file_path = os.path.join(folder, file_name)
        with open(file_path, "r", encoding="utf-8") as f:
            text += f.read() + "\n\n"  # separator between files    

    with open('final/output_final.txt', "w", encoding="utf-8") as f:
        f.write(text)

    return text

merge_txt(path)
'''
tool = TXTSearchTool(txt="final/output_final.txt",
    config=dict(
        llm=dict(
            provider="google", # or google, openai, anthropic, llama2, ...
            config=dict(
                api_key='',
                model="gemini-2.5-flash",
                temperature=0.5,
            ),
        ),        
        embedder=dict(
            provider="google", # or openai, ollama, ...
            config=dict(
                model="models/embedding-001",
                task_type="retrieval_document",
                # title="Embeddings",
            ),
        ),
    )
)





agent = Agent(
    role="Text Search Agent",
    goal="You will search the Text file for the answer to the question.  Use the tools to search the CSV file.",
    backstory="""You are a master at searching Text files.""",
    tools=[tool],
    verbose=True,
    allow_delegation=False,
    llm=llm
)

task = Task(
    description="Find the most relevant information related to: {question}. Searrch through the text file, and summarize what youve found. Make sure it is relevant to {question}",
    expected_output="1-2 Paragraph answer.\nConfidence Level:1-100 Score",
    tools=[tool],
    agent=agent,
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=True,
    process=Process.sequential,
)

question = st.chat_input("Enter a question about the text file: ")
if question:
    result = crew.kickoff(inputs={"question": question})
    st.write(result.raw)



'''
