import os
import asyncio
import json
from dotenv import load_dotenv
from smolagents import LiteLLMModel, CodeAgent
from models.schemas import Candidate
from agents.tools import calculate_experience, skill_match_validator
from utils.logger import logger

load_dotenv()


class ScreeningAgent:
    def __init__(self):
        self.model_configs = [
            {"id": "groq/llama-3.3-70b-versatile", "api_key": os.getenv("GROQ_API_KEY")},
            ]

    async def screen(self, cv_text: str, jd_text: str) -> Candidate:
        prompt = f"""
        Analyze the CV and JD provided below. 
        1. Use 'calculate_experience' to get the exact total years of experience.
        2. Use 'skill_match_validator' to get the match score.
        3. Construct the final response using THESE EXACT VALUES.

        JD: {jd_text}
        CV: {cv_text[:3000]}

        Final task: Return ONLY a JSON object:
        {{
            "name": "Full Name",
            "email": "Email Address",
            "years_of_experience": [VALUE FROM TOOL],
            "primary_skills": [LIST],
            "match_score": [SCORE FROM TOOL],
            "reasoning": "1-sentence summary"
        }}
        """

        for config in self.model_configs:
            if not config["api_key"]:
                continue

            try:
                logger.info(f"Attempting screening with model: {config['id']}")

                current_model = LiteLLMModel(
                    model_id=config["id"],
                    api_key=config["api_key"]
                )

                agent = CodeAgent(
                    tools=[calculate_experience, skill_match_validator],
                    model=current_model,
                   max_steps=3
                )

                raw_result = agent.run(prompt)

                if isinstance(raw_result, dict):
                    json_str = json.dumps(raw_result)
                else:
                    clean_str = str(raw_result).replace("```json", "").replace("```", "").strip()
                    json_str = clean_str.replace("'", '"')

                return Candidate.model_validate_json(json_str)

            except Exception as e:
                logger.warning(f"Model {config['id']} failed. Error: {str(e)}")
                await asyncio.sleep(1)
                continue

        raise RuntimeError("All AI models failed or are unavailable.")