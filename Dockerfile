FROM python:3.11

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

ARG APP_PATH=/var/app

WORKDIR ${APP_PATH}

COPY ./app ${APP_PATH}
COPY ./start.sh /
RUN chmod +x /start.sh

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
