FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN ls -l /app && pip install --no-cache-dir -r requirements.txt
RUN playwright install --with-deps chromium

COPY . .

CMD ["python", "mcp_job.py"]
