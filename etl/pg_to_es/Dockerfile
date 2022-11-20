FROM python:3.10 as base

WORKDIR /app

COPY . .

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt --no-cache-dir

CMD ["python", "etl.py"]
