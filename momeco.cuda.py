#!/usr/bin/env python

# --- by WOLFBED (c) 2022

# --- notes ////////////////////////////////////////////////////////////////////////////////////////////////////////////
"""

momeco.cuda.py : MOtion MEdia COnverter
                 (cuda edition)

---------


1. place files to convert in ToConvert/ dir
2. run $ momeco.py
3. converted files will materialize in Converted/ dir


NB : - currently only converts to mp4
     - currently only converts from gif, webm, mkv, mts, mpeg

---------

REQUIRES: - python
          - ffmpeg


"""
# --- imports //////////////////////////////////////////////////////////////////////////////////////////////////////////

import shell_colors as clic
from sys import exit
from subprocess import run
from os import popen

# --- ~statics /////////////////////////////////////////////////////////////////////////////////////////////////////////

# paths
FRO = "ToConvert/"
TOO = "Converted/"

# other
TYPES2DO = ["gif", "webm", "mkv", "MTS", "mpeg"]

# --- actions //////////////////////////////////////////////////////////////////////////////////////////////////////////

for t in TYPES2DO:

    def x2mp4(ext,fromhere,tohere) :

        FIFS = popen(f'find {fromhere} -name "*.{ext}"', "r").readlines()

        FIFFERS = []

        for f in FIFS :
            coif = f.replace("\n","").replace("./","")
            FIFFERS.append(coif)

        for FIF in FIFFERS:

            NEWFN = FIF.replace(f".{ext}", ".mp4").replace(f"{fromhere}","")

            CONVCMD = []

            # gifC = ["ffmpeg", "-i", f"{FIF}", "-movflags", "faststart", "-hide_banner", "-loglevel", "error", f"{tohere}{NEWFN}"]
            genericC = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-hwaccel", "cuda", "-i", f"{FIF}", "-c:v", "hevc_nvenc", "-preset", "fast", "-f", "mp4", f"{tohere}{NEWFN}"]

            match ext:
                case "gif" | "webm" | "mkv" | "MTS" | "mpeg" : CONVCMD = genericC
                case _:
                    print("extension not recognized")

            print(f" {clic.CC202}>>>>{clic.TRESET} {clic.CC2}looking at ......{clic.TRESET} {clic.CC83}{FIF} {clic.TRESET}")
            run(CONVCMD) # , "+"
            print(f" {clic.CC226}>>>>{clic.TRESET} {clic.CC2}new file made ... {clic.CC50}{tohere}{NEWFN}{clic.TRESET}")

    x2mp4(t,FRO,TOO)

print("All done.  Hopefully it all went well.  Bye!\n")

# --- end //////////////////////////////////////////////////////////////////////////////////////////////////////////////

exit()
