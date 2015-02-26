#!/bin/sh
cd /home/pi/test/mjpg-streamer/mjpg-streamer
./mjpg_streamer -i "./input_uvc.so -r QVGA -f 25" -o "./output_http.so -p 8080"

