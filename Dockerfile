FROM python:3.13-slim
WORKDIR /app

COPY ./requirements.txt /app/requriements.txt
RUN pip install --upgrade pip &&  \
    pip install -r requriements.txt
