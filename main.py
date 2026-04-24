import uvicorn
from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks
from services.parser import DocumentProcessor
from agents.screener import ScreeningAgent
from utils.logger import logger
import uuid

app = FastAPI(title="Agentic CV Screener Pro")
agent = ScreeningAgent()


@app.post("/v1/screen")
async def screen_cv(
        background_tasks: BackgroundTasks,
        file: UploadFile = File(...),
        job_description: str = Form(...)
):
    request_id = str(uuid.uuid4())
    logger.info("request_received", request_id=request_id, filename=file.filename)

    # 1. Parse PDF
    content = await file.read()
    cv_markdown = await DocumentProcessor.process_cv(content)

    # 2. Agentic Reasoning
    try:
        candidate_result = await agent.screen(cv_markdown, job_description)


        return {
            "request_id": request_id,
            "data": candidate_result
        }
    except Exception as e:
        logger.error("screening_failed", request_id=request_id, error=str(e))
        return {"error": "Processing failed", "details": str(e)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)