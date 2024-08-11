FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt
RUN mkdir ~/.streamlit

RUN apt-get update && apt-get install -y wget unzip && \

    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    apt-get clean
    