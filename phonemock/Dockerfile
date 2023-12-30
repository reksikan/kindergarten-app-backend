FROM python:3.10.7

COPY . .

RUN pip install -r ./requirements.txt

EXPOSE 8001

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8001", "main:app"]
