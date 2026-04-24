import structlog

def setup_logger():
    structlog.configure(
        processors=[
            structlog.processors.JSONRenderer() # Logs as JSON for ELK/Splunk
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
    )
    return structlog.get_logger()

logger = setup_logger()