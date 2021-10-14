FROM python:3.8.12-slim
RUN apt update 
RUN apt install -y gcc build-essential
#RUN rm -rf /var/lib/apt/lists/* \
#    && pip install cryptography \
#    && apt purge -y --auto-remove gcc build-essential
RUN apt install -y ffmpeg

WORKDIR /app
RUN mkdir /live
# RUN mkdir /app/bin

RUN pip3 install pipenv

EXPOSE 8000

COPY Pipfile* ./
RUN pipenv sync

COPY . .

ENTRYPOINT ["./scripts/docker-entrypoint.sh"]
