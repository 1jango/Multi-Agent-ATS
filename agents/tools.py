from smolagents import tool
from datetime import datetime
from dateutil import parser


@tool
def calculate_experience(employment_periods: list[dict]) -> float:
    """
    Calculates total years of experience from a list of employment periods.
    Function is designed to be able to recognize different types of date formats to prevent errors.
    Args:
    employment_periods: A list of dictionaries where each dict contains 'start_date' and 'end_date' (use 'present' for current jobs).
    """
    total_months = 0
    for period in employment_periods:
        start = parser.parse(period['start_date'])
        end_str = period.get('end_date')
        if end_str and end_str.lower() != 'present':
            end = parser.parse(end_str)
        else:
            end = datetime.now()

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
    found = []
    req_lower =[r.lower() for r in required_skills]
    for skill in candidate_skills:
        skill_lower = skill.lower()

        for req in req_lower:
            if req in skill_lower:
                found.append(skill)
                break

    if len(required_skills) > 0: score = len(found) / len(required_skills) * 100
    else: score = 0

    return {"overlap": found, "score": min(score, 100)}
