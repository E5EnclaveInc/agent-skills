#!/bin/bash
# One video at a time: download 360p -> capture frames at chapter timestamps -> delete video
# Usage: capture_frames.sh
set -u
mkdir -p /tmp/videolearn/frames
cap() {
  VID="$1"; shift
  echo "=== $VID ==="
  yt-dlp --no-check-certificate --extractor-args "youtube:player_client=android" \
    -f "bv*[height<=360]+ba/b[height<=360]/w" -o "/tmp/videolearn/tmp_${VID}.%(ext)s" \
    "https://www.youtube.com/watch?v=${VID}" 2>&1 | grep -E "^ERROR" | head -2
  mkdir -p "/tmp/videolearn/frames/${VID}"
  i=0
  for ts in "$@"; do
    i=$((i+1))
    fname=$(echo "$ts" | tr ':' '-')
    ffmpeg -y -v error -ss "$ts" -i "/tmp/videolearn/tmp_${VID}.mp4" \
      -frames:v 1 -q:v 4 "/tmp/videolearn/frames/${VID}/${i}_${fname}.jpg" 2>/dev/null \
    || echo "frame fail $VID $ts"
  done
  rm -f "/tmp/videolearn/tmp_${VID}.mp4"
  echo "CAPTURED ${VID}: $(ls /tmp/videolearn/frames/${VID} | wc -l) frames"
}
# Example calls (video id + chapter timestamps):
# cap <VIDEO_ID> 0:45 3:05 4:15
echo "ALL DONE"
