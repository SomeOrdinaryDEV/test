from crewai.tools import BaseTool
import requests
import json
import os
from dotenv import load_dotenv

import nltk
nltk.download('punkt', quiet=True)
from transformers import pipeline

pipe = pipeline("text-classification", model="ProsusAI/finbert", framework="pt", truncation=True, max_length=512)

load_dotenv()

class SerperNewsTool(BaseTool):
    name: str = "Serper News Tool"
    description: str = "Search the internet for news, returns with news snippet and sentiment"
    def search_news(self, query: str):
        """
        Developer-friendly method.
        Returns a Python list of dicts (easy for local testing).
        """
        url = "https://google.serper.dev/news"
        payload = json.dumps({
            "q": query,
            "num": 10,
            "location": "India",
            "gl": "in",
            "autocorrect": False,
            "tbs":"qdr:y"
        })
        headers = {
            'X-API-KEY': os.getenv('SERPER_API_KEY'),
            'Content-Type': 'application/json'
        }

        response = requests.post(url, headers=headers, data=payload)

        # Extract only the 'news' property
        news_data = response.json().get('news', [])

        # Cleaned format for dev usage
        cleaned = [
            {
                "title": item.get("title"),
                "link": item.get("link"),
                "snippet": item.get("snippet"),
                "score":pipe(item.get("snippet", []))
            }
            for item in news_data
        ]

        return cleaned

    def _run(self, query: str) -> str:
        """
        CrewAI agent-friendly method.
        Returns JSON string (agents work better with text).
        """
        results = self.search_news(query)
        return json.dumps(results, indent=2)