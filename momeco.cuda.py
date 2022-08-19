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
#FRO = "ToConvert/"
FRO = "/home/pierre/Projects/FuckinClipShowMagicMon/generic_video/"
#TOO = "Converted/"
TOO = "/home/pierre/Projects/FuckinClipShowMagicMon/generic_video/done/"

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

            # --- options - start --------------------------------------------------------------------------------------

            # result in this codec, options are h264, h265
            ReCo = "h264"

            # encoder speed, options are veryslow slower slow medium fast faster veryfast superfast ultrafast
            SPee = "superfast"

            # ?
            Tune = "fastdecode"
            """
            film – use for high quality movie content; lowers deblocking
            animation – good for cartoons; uses higher deblocking and more reference frames
            grain – preserves the grain structure in old, grainy film material
            stillimage – good for slideshow-like content
            fastdecode – allows faster decoding by disabling certain filters
            zerolatency – good for fast encoding and low-latency streaming
            """

            # --- options - end ----------------------------------------------------------------------------------------

            # put real codec command name here
            match ReCo:
                case "h265":
                    ReCo = "hevc_nvenc"
                case "h264":
                    ReCo = "h264"

            # tune stuffs
            match Tune:
                case "film":
                    Tune = f'{Tune}'
                case "animation":
                    Tune = f'{Tune}'
                case "grain":
                    Tune = f'{Tune}'
                case "stillimage":
                    Tune = f'{Tune}'
                case "fastdecode":
                    Tune = f'{Tune}'
                case "zerolatency":
                    Tune = f'{Tune}'
                case _:
                    Tune = "fastdecode"

            # full conversion command
            genericC = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-hwaccel", "cuda", "-i", f"{FIF}", "-c:v", f"{ReCo}", "-preset", f"{SPee}", "-tune", f"{Tune}", "-f", "mp4", f"{tohere}{NEWFN}"]

            # determine if input file extension is actionable, I know this sucks and should be based on codec of the stream, but for now ...
            match ext:
                case "gif" | "webm" | "mkv" | "MTS" | "mpeg" : CONVCMD = genericC
                case _:
                    print("extension not actionable")

            print(f" {clic.CC202}>>>>{clic.TRESET} {clic.CC2}looking at ......{clic.TRESET} {clic.CC83}{FIF} {clic.TRESET}")
            run(CONVCMD) # , "+"
            print(f" {clic.CC226}>>>>{clic.TRESET} {clic.CC2}new file made ... {clic.CC50}{tohere}{NEWFN}{clic.TRESET}")

    x2mp4(t,FRO,TOO)

print("All done.  Hopefully it all went well.  Bye!\n")

# --- end //////////////////////////////////////////////////////////////////////////////////////////////////////////////

exit()