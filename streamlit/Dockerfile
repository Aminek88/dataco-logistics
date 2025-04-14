FROM python:3.9-slim
WORKDIR /streamlit
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# CMD ["streamlit", "run", "dashboards/app.py", "--server.port", "8501"]
CMD ["tail", "-f", "/dev/null"]