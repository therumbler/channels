FROM python:3.7.4-alpine
WORKDIR /app
RUN mkdir /live
RUN mkdir /app/bin

EXPOSE 8080
RUN apk add ffmpeg

COPY ./docker-entrypoint.sh .

ENTRYPOINT ["./docker-entrypoint.sh"]
