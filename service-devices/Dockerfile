FROM python:3.8-slim
WORKDIR /app
EXPOSE 8180

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
CMD ["uvicorn", "devices:app", "--host", "0.0.0.0", "--port", "8180"]