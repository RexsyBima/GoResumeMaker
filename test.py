from unittest import TestCase
import os
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.deepseek import DeepSeekProvider


load_dotenv()

class TestAgent(TestCase):
    def test_run_agent(self):
        DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
        assert DEEPSEEK_API_KEY is not None
        model = OpenAIModel(
            'deepseek-chat',
            provider=DeepSeekProvider(api_key=DEEPSEEK_API_KEY),
        )
        agent = Agent(model)
        result = agent.run_sync("is this working?")
        print(result)
        self.assertTrue(bool(result))
