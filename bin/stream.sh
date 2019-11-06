#!/bin/bash


#INPUT="http://192.168.1.15:5004/auto/v9.1?transcode=mobile"
#INPUT="http://10.0.1.2:5004/auto/v7.1?transcode=mobile"
INPUT=$1
AUDIO_OPTS="-c:a aac -b:a 160000 -ac 2"
VIDEO_OPTS=""
OUTPUT_HLS="-hls_time 10 -hls_list_size 10 -start_number 1"
ffmpeg -i $INPUT -y $AUDIO_OPTS $VIDEO_OPTS $OUTPUT_HLS /Users/benjaminrumble/Documents/stuff/hdhomerun/live/stream.m3u8