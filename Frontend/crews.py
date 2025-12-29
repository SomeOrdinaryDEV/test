from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from tools.custom_tool import SerperNewsTool
from google import genai
from dotenv import load_dotenv
load_dotenv()
import os
from pydantic import BaseModel, Field
from typing import List, Dict
os.environ['GEMINI_API_KEY'] = os.getenv('GEMINI_API_KEY')


news_tool = SerperNewsTool(max_usage_count=4)
tool = SerperDevTool(max_usage_count=4)

llm = LLM(model="gemini/gemini-2.0-flash",
          temperature=0.6,
          )

class FinFormat(BaseModel):
    score: int 
    company: str
    key_insights: str
    red_flags: List[str]
    strengths: List[str]
    growth_rate: int
    revenue: int
    liquidity: int
    profit_margins: int

class NewsFormat(BaseModel):
    score: int 
    company: str
    key_insights: str
    red_flags: List[str]
    strengths: List[str]
    product_quality_rating: int
    environmental_rating: int


class CompanyOverview(BaseModel):
    legal_name: str
    industry: str
    primary_activities: List[str]
    locations_of_operation: int
    short_summary: str

@CrewBase
class TrialCrew:
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    @agent
    def finance_wiz(self) -> Agent:
        return Agent(
        config=self.agents_config['finance_wiz'],
        llm=llm,
        tools=[
            tool,
            news_tool
        ]
    )
    
    @task
    def finance_risk_score(self) -> Task: 
        return Task(
            config=self.tasks_config['finance_risk_score'],
            agent=self.finance_wiz(),
            output_json=FinFormat
        )
    
    @agent
    def news_wiz(self) -> Agent:
        return Agent(
            config=self.agents_config['news_wiz'],
            llm=llm,
            tools=[
                news_tool,
                tool,
            ]
        )
    
    @task
    def news_risk_score(self) -> Task: 
        return Task(
            config=self.tasks_config['news_risk_score'],
            agent=self.news_wiz(),
            output_json=NewsFormat
        )
    @agent
    def gen_wiz(self) -> Agent:
        return Agent(
            config=self.agents_config['gen_wiz'],
            llm=llm,
            tools=[
                tool
            ]
        )
    
    @task
    def describe_task(self) -> Task: 
        return Task(
            config=self.tasks_config['describe_task'],
            agent=self.gen_wiz(),
            output_json=CompanyOverview
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,  
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,            
        )