FROM python:3.7.4-alpine
EXPOSE 5005
RUN apk add ffmpeg
#CMD ["ffmpeg", "-i", "http://192.168.1.15:5004/auto/v9.1?transcode=mobile", "-f", "mpegts", "tcp://127.0.0.1:5006"]

CMD ["ffmpeg",  \
    #"-v", "debug", \ 
    "-fflags", "nobuffer", \
    "-i", "http://192.168.1.15:5004/auto/v9.1?transcode=mobile", \
    "-r", "15", \
    "-vsync", "2", \
    "-copyts", \
    "-copytb", "1", \
    "-codec", "copy", \
    "-map", "0", \
    "-f", "segment", \
    "-segment_time", "2", \
    "-segment_list", "stream.m3u8", \
    "-segment_format", "mpegts", \
    "-segment_list_flags", "+live", \
    "stream-%09d.ts"]