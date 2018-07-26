#!/usr/bin/python3

from subprocess import Popen, PIPE, check_output
from time import sleep
import sys

def run(cmd):
    return check_output(cmd, stderr=sys.stderr, encoding="utf-8")

def fonts(name="fonf", size=16):
    return ("xft:{}:pixelsize={}".format(name, size),
            "xft:{}:bold:pixelsize={}".format(name, size))

def xephyr_run(display):
    # Use dimensions that are (hopefully) larger than urxvt will need.
    dimensions = "1400x1000"
    return Popen(["Xephyr", "-screen", dimensions, "-resizeable", display])

def ffmpeg_run(display, dimensions, duration, output="output.mp4"):
    return Popen(["ffmpeg", "-video_size", dimensions, "-framerate", "10",
                    "-f", "x11grab", "-t", duration, "-i", display, output],
                 stderr=PIPE)

def urxvt_run(display, script):
    font_norm, font_bold = fonts()
    return Popen(["urxvt", "-display", display, "-fn", font_norm,
                    "-fb", font_bold, "-e", script])

def urxvt_dimensions(display):
    stdout = run(["xwininfo", "-display", display, "-root", "-children",
                    "-stats"])
    lines = map(str.strip, stdout.splitlines())
    lines = filter(lambda line: ": " in line, lines)
    stats = dict(map(lambda line: line.split(": ", 1), lines))
    width = stats["Width"]
    height = stats["Height"]
    print("urxvt dimensions = {}x{}".format(width, height))
    return "x".join([width, height])

script = "/home/pup/demo-script/replay.sh"
script = "/usr/bin/nvim"

display = ":1"
duration = "10"

xephyr = xephyr_run(display)
sleep(1)

urxvt  = urxvt_run(display, script)
sleep(1)
dimensions = urxvt_dimensions(display)

ffmpeg = ffmpeg_run(display, dimensions, duration)


ffmpeg.communicate()
urxvt.communicate()
xephyr.kill()
