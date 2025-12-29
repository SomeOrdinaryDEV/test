import streamlit as st
import os
import time
import random
from crewai import Agent, Task, LLM, Crew, Process
from crewai_tools import TXTSearchTool, SerperDevTool
import os
from dotenv import load_dotenv
import streamlit as st
from google import genai
import streamlit as st
import json

load_dotenv()
path = "output"
tool2 = SerperDevTool()

llm = LLM(model="gemini/gemini-2.5-flash",
          temperature=0.5,)

def merge_txt(folder):
    text = ""
    for file_name in os.listdir(folder):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder, file_name)
            with open(file_path, "r", encoding="utf-8") as f:
                text += f.read() + "\n\n"  # separator between files    
    
    with open('final/output_final.txt', "w", encoding="utf-8") as f:
        f.write(text)

    return text

merge_txt(path)

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





st.set_page_config(
    page_title="EY Supplier Procurement",
    page_icon="https://upload.wikimedia.org/wikipedia/commons/3/34/EY_logo_2019.svg",
    layout="wide",
    initial_sidebar_state="expanded", 
)


# Streamed response generator


# Wide page layout for columns
st.set_page_config(layout="wide")

# Create three columns: left sidebar, main content, right sidebar (chatbot)
col_left, col_main, col_right = st.columns([1, 4, 2])

# ---------------- Left Sidebar ----------------
with col_left:
    st.header("Options")
    dropdown_option = st.selectbox(
        "Choose an option:",
        ["Option 1", "Option 2", "Option 3"]
    )
    st.write(f"You selected: {dropdown_option}")

# ---------------- Main Content ----------------
with col_main:
    st.title("Supplier Procurement Risk Assessment")
    st.write("Ratings of suppliers")

# ---------------- Right Sidebar (Chatbot) ----------------


with col_right:
    st.markdown('', unsafe_allow_html=True)
    st.header("AI Chatbot")
    st.write(":wave: Welcome! How can I assist you today?")
    user_input = st.text_input("Ask your question:")
    if user_input:
        st.write(f"You asked: {user_input}")
        st.write("AI response would go here.")
        st.markdown('', unsafe_allow_html=True)


st.title("Simple chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = crew.kickoff(inputs={"question": prompt})

        response = st.write(response.raw)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response.raw})



