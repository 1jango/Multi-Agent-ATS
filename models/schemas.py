from typing import List
from pydantic import BaseModel, Field

class Candidate(BaseModel):
    name: str = Field(..., description="Full name of the candidate")
    email: str = Field(..., description="E-mail address of the candidate")
    years_of_experience: float = Field(..., description="Total relevant years of experience")
    primary_skills: List[str] = Field(..., description="List of core technical skills found")
    match_score: int = Field(..., ge=0, le=100, description="Overall match score (0-100)")
    reasoning: str = Field(..., description="Brief explanation for the score")

class ScreeningRequest(BaseModel):
    job_description: str
