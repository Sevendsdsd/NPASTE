FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 5000 5001

CMD ["python", "src/main.py", "--dashboard"]
