FROM python:3.10-alpine

WORKDIR /bot
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY /bot .


CMD ["python", "main.py", "0.0.0.0:8000"]
EXPOSE 8000