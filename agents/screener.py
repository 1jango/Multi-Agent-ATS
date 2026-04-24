import os
import asyncio
from dotenv import load_dotenv
from smolagents import CodeAgent, LiteLLMModel
from models.schemas import Candidate
from agents.tools import calculate_experience, skill_match_validator
from pydantic_ai import Agent as PydanticAgent
from litellm import ServiceUnavailableError
from utils.logger import logger

load_dotenv()

class ScreeningAgent:
    def __init__(self):
        self.model = LiteLLMModel(
            model_id="gemini/gemini-3-flash-preview",
            api_key=os.getenv("GEMINI_API_KEY")
        )

        self.agent = CodeAgent(
            tools=[calculate_experience, skill_match_validator],
            model=self.model,
            add_base_tools=True
        )

    async def screen(self, cv_text: str, jd_text: str) -> Candidate:
        prompt = f"""
        You are an expert HR Architect. Match this CV to the JD.
        JOB DESCRIPTION: {jd_text}
        CANDIDATE CV (Markdown): {cv_text}
        ... (rest of your prompt) ...
        """

        max_retries = 3
        delay = 2

        for attempt in range(max_retries):
            try:

                result = self.agent.run(prompt)

                validator = PydanticAgent('google-gla:gemini-3-flash-preview')
                validated_data = await validator.run(f"Transform it into a structured JSON: {result}",
                                                     result_type = Candidate)


                return validated_data.data

            except ServiceUnavailableError:
                if attempt < max_retries - 1:
                    logger.warning(f"Gemini busy, retrying in {delay}s... (Attempt {attempt + 1})")
                    await asyncio.sleep(delay)
                    delay *= 2
                else:
                    logger.error("Gemini service unavailable after max retries.")
                    raise