FROM mcr.microsoft.com/playwright/python:v1.46.0-jammy

WORKDIR /app

# Install dependencies (API + scraper + optional pandas for debug script)
RUN pip install --no-cache-dir fastapi "uvicorn[standard]" playwright pandas \
    && python -m playwright install --with-deps chromium

# Copy source
COPY app ./app
COPY main.py ./
COPY debug.py ./

# Ensure log directory exists for traces/logs
RUN mkdir -p /app/app/log

ENV PYTHONUNBUFFERED=1 \
    HEADLESS=true \
    NFPA_QUERY="NFPA 70" \
    TRACE_PATH="./app/log/handler_trace.zip"

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
