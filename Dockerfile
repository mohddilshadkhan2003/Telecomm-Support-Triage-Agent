FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY finalproject/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY finalproject ./finalproject
WORKDIR /app/finalproject
RUN mkdir -p data
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
