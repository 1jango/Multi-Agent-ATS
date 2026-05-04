from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from services.parser import DocumentProcessor
from agents.screener import ScreeningAgent
from utils.logger import logger
import uuid

router = APIRouter(prefix="/v1", tags=["Screening"])
agent = ScreeningAgent()


@router.post("/screen")
async def screen_cv(
        file: UploadFile = File(...),
        job_description: str = Form(...)
):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")

    request_id = str(uuid.uuid4())
    logger.info("request_received", request_id=request_id, filename=file.filename)

    try:
        # 1. Parse PDF using PyMuPDF4LLM logic
        pdf_content = await file.read()
        cv_markdown = DocumentProcessor.to_markdown(pdf_content)

        # 2. Agentic Reasoning
        # Ensure your ScreeningAgent.run_screening is async or handled properly
        result = await agent.run_screening(cv_markdown, job_description)

        return {"request_id": request_id, "candidate_analysis": result}

    except Exception as e:
        logger.error("screening_failed", request_id=request_id, error=str(e))
        raise HTTPException(status_code=500, detail="Internal processing error")
