# BUILDER #
FROM python:3.9-alpine3.14 as builder

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev \
    && apk add libffi-dev libressl-dev \
    && apk add --no-cache jpeg-dev zlib-dev libjpeg \
    && apk add rust cargo

RUN pip install --upgrade pip
RUN pip install Pillow
RUN pip install flake8
COPY . .

COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

# FINAL #
FROM python:3.9-alpine3.14

RUN mkdir -p /home/app

RUN addgroup -S app && adduser -S app -G app

ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
RUN mkdir $APP_HOME/media
WORKDIR $APP_HOME

RUN apk update && apk add libpq
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

COPY ./entrypoint.sh $APP_HOME

COPY . $APP_HOME

RUN chown -R app:app $APP_HOME


USER app

ENTRYPOINT ["/home/app/web/entrypoint.sh"]
