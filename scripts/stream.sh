#!/bin/sh
#set -euxo pipefail
set -eux

INPUT=$1
FILE_PATH=/live/$2

if test -f $FILE_PATH ; then
    rm $FILE_PATH/*.* || true
else
    echo "making directory $FILE_PATH"
    mkdir $FILE_PATH || true 
fi

exec ffmpeg  \
    -hide_banner \
    -loglevel error \
    -i $INPUT \
    -acodec aac \
    -ac 2 \
    -vcodec libx264 \
    -map 0 \
    -f hls \
    -hls_time 1 \
    -hls_list_size 20 \
    -hls_flags delete_segments \
    $FILE_PATH/stream.m3u8
