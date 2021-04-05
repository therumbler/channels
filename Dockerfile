FROM python:3.8.7-alpine
WORKDIR /app
RUN mkdir /live
# RUN mkdir /app/bin

RUN pip3 install pipenv

EXPOSE 8080
RUN apk add ffmpeg

COPY Pipfile* .
RUN pipenv sync


COPY . .

ENTRYPOINT ["./scripts/docker-entrypoint.sh"]
