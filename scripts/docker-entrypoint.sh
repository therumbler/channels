#!/bin/sh
echo "removing files ..."
rm /live/*.ts
rm /live/*.m3u8

ffmpeg  \
    -i http://10.0.1.238:5004/auto/v29.1?transcode=mobile \
    -acodec aac \
    -ac 2 \
    -vcodec libx264 \
    -map 0 \
    -f hls \
    -hls_time 1 \
    -hls_list_size 20 \
    -hls_flags delete_segments \
    /live/stream.m3u8
