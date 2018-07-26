#!/usr/bin/python3

from subprocess import Popen, PIPE, check_output
from time import sleep
import sys

def run(cmd, display):
    env = {"DISPLAY": display}
    return check_output(cmd, env=env, stderr=sys.stderr, encoding="utf-8")

def fonts(name="fonf", size=16):
    return ("xft:{}:pixelsize={}".format(name, size),
            "xft:{}:bold:pixelsize={}".format(name, size))

def xephyr_start(display):
    # Use dimensions that are (hopefully) larger than urxvt will need.
    dimensions = "1400x1000"
    return Popen(["Xephyr", "-screen", dimensions, "-resizeable", display])

def ffmpeg_start(display, dimensions, duration, output="output.mp4"):
    return Popen(["ffmpeg", "-video_size", dimensions, "-framerate", "10",
                    "-f", "x11grab", "-t", duration, "-i", display, output],
                 stderr=PIPE)

def urxvt_start(display, script):
    font_norm, font_bold = fonts()
    return Popen(["urxvt", "-display", display, "-fn", font_norm,
                    "-fb", font_bold, "-e", script])

def normalize_line(line):
    parts = line.split(":", 1)
    parts = map(str.strip, parts)
    parts = map(str.lower, parts)
    return list(parts)

def parse_xwininfo(text):
    lines = text.splitlines()
    lines = filter(lambda line: ":" in line, lines)
    lines = map(lambda line: normalize_line(line), lines)
    return dict(lines)

def urxvt_dimensions(display, pid):
    win_id = run(["xdotool", "search", "--pid", str(pid)], display).strip()
    xwinfo = run(["xwininfo", "-id", win_id], display)
    stats  = parse_xwininfo(xwinfo)
    return "x".join([stats["width"], stats["height"]])

script = "/home/pup/demo-script/replay.sh"
script = "/usr/bin/nvim"

display = ":1"
duration = "10"

xephyr = xephyr_start(display)
sleep(1)

urxvt  = urxvt_start(display, script)
sleep(1)
dimensions = urxvt_dimensions(display, urxvt.pid)

ffmpeg = ffmpeg_start(display, dimensions, duration)

# Wait for urxvt to finish.
urxvt.communicate()

# The script is done -- tell ffmpeg to quit.
ffmpeg.terminate()

# Wait for ffmpeg to finish.
ffmpeg.communicate()

# Close Xephyr.
xephyr.terminate()
