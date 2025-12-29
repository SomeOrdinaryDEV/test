from crewai import Agent, Task, LLM, Crew, Process
from crewai_tools import TXTSearchTool, SerperDevTool
import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()
from google import genai
import json
import random
import time


client = genai.Client(api_key='AIzaSyB7OF3ppieHCE09zCWL2a-B874XSYpzP3g')
llm = LLM(model="gemini/gemini-2.5-flash",
          temperature=0.7,)


def merge_txt(folder):
    text = ""
    for file_name in os.listdir(folder):
        file_path = os.path.join(folder, file_name)
        with open(file_path, "r", encoding="utf-8") as f:
            text += f.read() + "\n\n"  # separator between files    

    with open('final/output_final.txt', "w", encoding="utf-8") as f:
        f.write(text)

    return text

merge_txt("output")

def response_generator(response):
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


tool = TXTSearchTool(txt="final/output_final.txt",
    config=dict(
        llm=dict(
            provider="google", # or google, openai, anthropic, llama2, ...
            config=dict(
                api_key='AIzaSyB7OF3ppieHCE09zCWL2a-B874XSYpzP3g',
                model="gemini-2.0-flash",
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
web_tool = SerperDevTool(max_usage_limit=4)

agent = Agent(
    role="Supplier Intelligence & Decision Agent",
    goal="""Answer the question by ingesting, searching, and analyzing supplier information from text and JSON sources.
        Extract relevant facts, compare across suppliers, and synthesize insights.
        Provide clear recommendations on credibility, compliance, risk, and alignment
        with procurement requirements.""",
    backstory="""You are an expert procurement analyst with deep knowledge of supplier risk,
        ESG considerations, compliance standards, and market dynamics. You excel at
        scanning unstructured text and structured data, identifying what matters,
        and making sound judgments. """,
    tools=[tool, ],
    verbose=True,
    allow_delegation=False,
    llm=llm
)
task = Task(
    description="Find the most relevant information related to: {question}. Search through the text file, and summarize what youve found. Make sure it is relevant to {question}. If it is not relevent, THEN ONLY SEARCH THE WEB to finish task",
    expected_output="""1. 1-2 Paragraph answering {question}.
    \nWith a new line, give confidence level.
    2. Confidence Level:1-100""",
    tools=[tool, web_tool],
    agent=agent,
)   
crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=True,
    process=Process.sequential,
)


st.header("Procurement Chatbot")
st.subheader("Ask questions about procurement process", divider="rainbow")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask question about procurement process"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):  
        result = crew.kickoff(inputs={"question": prompt})
        response = st.write_stream(response_generator(result.raw))
    st.session_state.messages.append({"role": "assistant", "content": result.raw})
