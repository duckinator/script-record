#!/usr/bin/python3

from subprocess import Popen, PIPE, check_output
from time import sleep
import sys

def run(cmd, env=None):
    return check_output(cmd, env=env, stderr=sys.stderr, encoding="utf-8")

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

def normalize_line(line):
    parts = line.split(":", 1)
    parts = map(str.strip, parts)
    parts = map(str.lower, parts)
    return list(parts)

def urxvt_dimensions(display, pid):
    env = {"DISPLAY": display}
    win_id = run(["xdotool", "search", "--pid", str(pid)], env=env).strip()
    lines = run(["xwininfo", "-display", display, "-id", win_id]).splitlines()
    lines = map(lambda line: normalize_line(line), lines)
    lines = filter(lambda line: len(line) == 2, lines)
    stats = dict(lines)
    return "x".join([stats["width"], stats["height"]])

script = "/home/pup/demo-script/replay.sh"
script = "/usr/bin/nvim"

display = ":1"
duration = "10"

xephyr = xephyr_run(display)
sleep(1)

urxvt  = urxvt_run(display, script)
sleep(1)
dimensions = urxvt_dimensions(display, urxvt.pid)

ffmpeg = ffmpeg_run(display, dimensions, duration)

urxvt.communicate()
ffmpeg.communicate()
xephyr.kill()
