FROM python:3.7.3-alpine3.9 
COPY requirements.txt .
RUN pip install -r requirements.txt
WORKDIR /srv
COPY code/ ./
EXPOSE 8000
ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:8000", "--workers=1", "http_api.app"]
CMD ["--access-logfile=-"]
