FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x *_rag/agent.py test_ollama_connection.py

CMD ["python", "langchain_rag/agent.py"]
