#!/bin/bash

FONT=fonf
FSIZE=16
Xephyr -screen 1360x760 -resizeable :1 &
sleep 1

ffmpeg -video_size 1046x630 -framerate 10 -f x11grab -t 60 -i :1 output.mp4 &
sleep 1

export DISPLAY=:1
urxvt -fn "xft:$FONT:pixelsize=$FSIZE" -fb "xft:$FONT:bold:pixelsize=$FSIZE" -e /home/pup/demo-script/replay.sh
