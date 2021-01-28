FROM python:latest

ENV PKGS="pip python-telegram-bot"

WORKDIR /app
COPY . .
RUN pip3 install -U ${PKGS}

CMD ["python3", "./main.py"]