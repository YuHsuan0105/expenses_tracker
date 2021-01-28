FROM python:latest

ENV PKGS="python-telegram-bot pymysql matplotlib"

WORKDIR /app
COPY . .
RUN pip3 install -U ${PKGS}

CMD ["python3", "./main.py"]