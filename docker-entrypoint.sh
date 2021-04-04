#!/bin/sh
echo "removing files ..."
rm /live/*.ts
rm /live/*.m3u8

ffmpeg  \
    -i http://10.0.1.238:5004/auto/v9.1?transcode=mobile \
    -r 15 \
    -codec copy \
    -copyts \
    -copytb 1 \
    -map 0 \
    -f hls \
    -hls_time 1 \
    -hls_list_size 20 \
    -hls_flags delete_segments \
    /live/stream.m3u8

#  -ac 2 \
    # -c:a aac \
#  -c:a aac \
    # -b:a 160000 \
#   -f segment \
    # -segment_time 2 \
  #  -segment_list stream.m3u8 \
#    "-vsync", "2", \
  #"-v", "debug", \ 
    # "-fflags", "nobuffer", \
    # "-segment_format", "mpegts", \
    # "-segment_list_flags", "+live", \
