FROM python:3.9-slim
WORKDIR /ml
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["mlflow", "server", "--host", "0.0.0.0", "--port", "5000"]