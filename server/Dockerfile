FROM python:3.11-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

HEALTHCHECK --interval=5s --timeout=5s --retries=5 --start-period=5s CMD curl -f 0.0.0.0:8000/ping || exit 1
