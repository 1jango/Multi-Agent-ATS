import pymupdf4llm
import tempfile
from fastapi import HTTPException
from utils.logger import logger


class DocumentProcessor:
    @staticmethod
    async def process_cv(file_bytes: bytes) -> str:
        try:
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=True) as tmp:
                tmp.write(file_bytes)
                tmp.flush()
                # Extract as Markdown for structural context
                md_text = pymupdf4llm.to_markdown(tmp.name)

                if not md_text or len(md_text.strip()) < 50:
                    raise ValueError("Document is empty or contains insufficient text.")

                return md_text
        except Exception as e:
            logger.error("pdf_parsing_failed", error=str(e))
            raise HTTPException(status_code=422, detail="Invalid or corrupted PDF.")