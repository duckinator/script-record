#!/usr/bin/python3

from subprocess import Popen, PIPE
from time import sleep

def fonts(name="fonf", size=16):
    return ("xft:{}:pixelsize={}".format(name, size),
            "xft:{}:bold:pixelsize={}".format(name, size))

def xephyr_run(display):
    # Set the dimensions to something that should (hopefully) be more than
    # urxvt needs.
    dimensions = "1000x1000"
    return Popen(["Xephyr", "-screen", dimensions, "-resizeable", display])

def ffmpeg_run(display, dimensions_tuple, duration, output="output.mp4"):
    dimensions = "x".join(dimensions_tuple)
    return Popen(["ffmpeg", "-video_size", dimensions, "-framerate", "10",
                    "-f", "x11grab", "-t", duration, "-i", display, output],
                 stderr=PIPE)

def urxvt_run(display, script):
    font_norm, font_bold = fonts()
    return Popen(["urxvt", "-display", display, "-fn", font_norm,
                    "-fb", font_bold, "-e", script])

def urxvt_dimensions(display):
    proc = Popen(["xwininfo", "-display", display, "-root", "-children",
                    "-stats"], stdout=PIPE, encoding="utf-8")
    stdout, _ = proc.communicate()
    lines = stdout.splitlines()
    lines = map(str.strip, lines)
    lines = filter(lambda line: ": " in line, lines)
    stats = dict(map(lambda line: line.split(": ", 1), lines))
    return (stats["Width"], stats["Height"])

script = "/home/pup/demo-script/replay.sh"
script = "/usr/bin/nvim"

display = ":1"
duration = "10"

xephyr = xephyr_run(display)
sleep(1)

urxvt  = urxvt_run(display, script)
width, height = urxvt_dimensions(display)
sleep(1)

ffmpeg = ffmpeg_run(display, (width, height), duration)


ffmpeg.communicate()
urxvt.communicate()
xephyr.kill()
