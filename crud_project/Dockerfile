FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "--access-logfile", "-", "--error-logfile", "-", "-b", "0.0.0.0:5000", "main:app"]
