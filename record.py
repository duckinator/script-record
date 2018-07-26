#!/usr/bin/python3

from subprocess import Popen, PIPE
from time import sleep

def fonts(name="fonf", size=16):
    return ("xft:{}:pixelsize={}".format(name, size),
            "xft:{}:bold:pixelsize={}".format(name, size))

def xephyr_run(dimensions, display):
    return Popen(["Xephyr", "-screen", dimensions, "-resizeable", display])

def ffmpeg_run(dimensions, display, duration, output="output.mp4"):
    return Popen(["ffmpeg", "-video_size", dimensions, "-framerate", "10",
                    "-f", "x11grab", "-t", duration, "-i", display, output],
                 stderr=PIPE)

def urxvt_run(dimensions, display, script):
    font_norm, font_bold = fonts()
    return Popen(["urxvt", "-display", display, "-fn", font_norm,
                    "-fb", font_bold, "-e", script])

script = "/home/pup/demo-script/replay.sh"
script = "/usr/bin/nvim"

dimensions = "1000x730"
display = ":1"
duration = "10"

xephyr = xephyr_run(dimensions, display)
sleep(1)
ffmpeg = ffmpeg_run(dimensions, display, duration)
sleep(1)
urxvt  = urxvt_run(dimensions, display, script)

ffmpeg.communicate()
urxvt.communicate()
xephyr.kill()
