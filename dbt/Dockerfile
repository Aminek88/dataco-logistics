FROM python:3.9-slim
WORKDIR /dbt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# CMD ["dbt", "run"]
CMD ["tail", "-f", "/dev/null"]