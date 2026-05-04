Agentic CV Screener


A high-performance ATS agent built with FastAPI and smolagents. This tool automates CV screening by converting PDFs to Markdown and using agentic reasoning to validate candidates against job descriptions.

Key Updates (v2.0)
•	Single-Agent Architecture: Migrated from a multi-agent setup to a unified CodeAgent for better state management and reliability.
•	Token Optimization: Significant reduction in token consumption through refined prompting and streamlined logic.
•	Tool-Use Logic: The agent now autonomously uses specialized Python tools (calculate_experience, skill_match_validator) for 100% mathematical accuracy in experience calculation.
•	Llama 3.3 Powered: Optimized for llama-3.3-70b-versatile via Groq for sub-second reasoning.


Tech Stack
•	Framework: FastAPI
•	Orchestration: smolagents by Hugging Face
•	Parsing: PyMuPDF4LLM (Markdown-based extraction)
•	Inference: Groq (Llama 3.3)
