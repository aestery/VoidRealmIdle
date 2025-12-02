FROM python:3.13

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY bot/ /app/bot
COPY core/ /app/core
COPY locales/ /app/locales/
COPY main.py /app/
COPY run_migrations.py /app/