FROM python:3.11

ENV DB_USER=${BACKEND_DB_USER}
ENV DB_PASSWORD=${BACKEND_DB_PASSWORD}
ENV DB_NAME=${DB_NAME}
ENV DB_HOST=${DB_HOST}

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "main.py"]
