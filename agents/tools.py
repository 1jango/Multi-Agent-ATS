from smolagents import tool
import re

from smolagents import tool
from datetime import datetime


@tool
def calculate_experience(employment_periods: list[dict]) -> float:
    """
    Calculates total years of experience from a list of employment periods.
    Args:
        employment_periods: A list of dicts with 'start_date' and 'end_date' (format: YYYY-MM).
    """
    total_months = 0
    for period in employment_periods:
        start = datetime.strptime(period['start_date'], "%Y-%m")
        # Handle 'Present' or missing end date
        end_str = period.get('end_date')
        end = datetime.strptime(end_str, "%Y-%m") if end_str and end_str.lower() != 'present' else datetime.now()

        diff = (end.year - start.year) * 12 + (end.month - start.month)
        total_months += diff

    return round(total_months / 12, 1)

@tool
def skill_match_validator(candidate_skills: list, required_skills: list) -> dict:
    """
    Compares extracted candidate skills against JD requirements.
    Args:
        candidate_skills: List of skills from CV.
        required_skills: List of skills from JD.
    """
    found = [s for s in candidate_skills if any(r.lower() in s.lower() for r in required_skills)]
    score = (len(found) / len(required_skills) * 100) if required_skills else 0
    return {"overlap": found, "score": min(score, 100)}