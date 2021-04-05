#!/bin/sh


#INPUT="http://192.168.1.15:5004/auto/v9.1?transcode=mobile"
#INPUT="http://10.0.1.2:5004/auto/v7.1?transcode=mobile"
INPUT=$1
ffmpeg  \
    -i INPUT \
    -acodec aac \
    -ac 2 \
    -vcodec libx264 \
    -map 0 \
    -f hls \
    -hls_time 1 \
    -hls_list_size 20 \
    -hls_flags delete_segments \
    /live/stream.m3u8
