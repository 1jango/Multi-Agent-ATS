# Agentic-CV-Screener

A high-performance, asynchronous AI recruitment system that automates CV screening using a multi-agent architecture. This project transforms raw PDF resumes into structured candidate profiles and evaluates them against specific job descriptions (JD).

## Key Features
- **Multi-Agent Architecture**: Uses a two-stage process combining `smolagents` for reasoning and `Pydantic-AI` for structured data validation.
- **Agentic Reasoning**: The system doesn't just match keywords; it analyzes professional experience, education, and skills semantically.
- **Python-Powered Tools**: Integrated custom tools for precise calculations (e.g., total years of experience) to prevent LLM "hallucinations" in math.
- **Infrastructure Resilience**: Implemented **Exponential Backoff** logic to handle API rate limits and 503 Service Unavailable errors gracefully.
- **Provider Agnostic**: Built on top of **LiteLLM**, allowing seamless switching between OpenAI (GPT-4o) and Google Gemini models.

## ️ Technical Stack
- **Backend**: FastAPI (Python 3.14+)
- **Orchestration**: `smolagents` (HuggingFace) & `Pydantic-AI`
- **LLM Gateway**: `LiteLLM`
- **Validation**: `Pydantic v2`
- **PDF Processing**: `PyMuPDF` / `Marker`

## Project Structure
```text
├── agents/          # AI Agent logic and custom tools
├── api/             # FastAPI routes and endpoint definitions
├── models/          # Pydantic schemas and data contracts
├── services/        # PDF parsing and core business logic
├── utils/           # Logging and resilience utilities
├── main.py          # Application entry point
└── requirements.txt # Project dependencies
