FROM python:3.11-slim
WORKDIR /app

COPY 02_worker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY 02_worker/ /app/
COPY 03_common/ /app/common/

CMD ["python", "main.py"]