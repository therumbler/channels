FROM python:3.7.4-alpine
WORKDIR /app
RUN mkdir /live
RUN mkdir /app/bin

EXPOSE 5005
RUN apk add ffmpeg
#CMD ["ffmpeg", "-i", "http://192.168.1.15:5004/auto/v9.1?transcode=mobile", "-f", "mpegts", "tcp://127.0.0.1:5006"]

COPY ./docker-entrypoint.sh .
# RUN chmod +x /app/bin/docker-entrypoint.sh

ENTRYPOINT ["./docker-entrypoint.sh"]

# CMD ["ffmpeg",  \
#     "-i", "http://10.0.1.238:5004/auto/v9.1?transcode=mobile", \
#     "-c:a", "aac", \
#     "-b:a", "160000", \
#     "-ac", "2", \
#     "-r", "15", \
#     "-copyts", \
#     "-copytb", "1", \
#     "-codec", "copy", \
#     "-map", "0", \
#     "-f", "segment", \
#     "-segment_time", "2", \
#     "-segment_list", "stream.m3u8", \
#     "stream-%09d.ts"]

#    "-vsync", "2", \
  #"-v", "debug", \ 
    # "-fflags", "nobuffer", \
    # "-segment_format", "mpegts", \
    # "-segment_list_flags", "+live", \