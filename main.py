#!/usr/bin/env python

# --- by P.W.R. Marcoux (c) 2021


# --- notes ////////////////////////////////////////////////////////////////////
"""
momeco.cuda.py : MOtion MEdia COnverter
---------
1. place files to convert in ToConvert/ dir
2. run $ momeco.py
3. converted files will materialize in Converted/ dir
NB : - currently only converts to mp4
     - currently only converts from gif, webm, mkv, mts, mpeg
"""
# --- imports //////////////////////////////////////////////////////////////////

import shell_colors as clic
from sys import exit
from subprocess import run
from os import popen
import os, time, sys

# --- ~statics /////////////////////////////////////////////////////////////////

# paths
FRO = "ToConvert/"
TOO = "Converted/"

# other
TYPES2DO = ["gif", "webm", "mkv", "MTS", "mpeg"]

# --- actions //////////////////////////////////////////////////////////////////

# -- check for dirs and presence of files //////////

# Specify path
convp = 'Converted'
toconvp = 'ToConvert'

# Check whether the specified
# path exists or not
isConvPExist = os.path.exists(convp)
isToConvPExist = os.path.exists(toconvp)

if isConvPExist == False:
    print("'Converted' dir doesn't exist.  Creating... ", end="")
    sys.stdout.flush()
    try:
        os.mkdir(convp)
        time.sleep(0.01)  # fake process
        print("Done.")
    except OSError as error:
        print(error)
        exit()

if isToConvPExist == False:
    print("'ToConvert' dir doesn't exist.  Creating... ", end="")
    sys.stdout.flush()
    try:
        os.mkdir(toconvp)
        time.sleep(0.01)  # fake process
        print("Done.")
    except OSError as error:
        print(error)
        exit()
    print("Be sure to place your video files in the 'ToConvert' dir before running again.  QUITTING.")
    exit()
elif isToConvPExist == True:
    print("'ToConvert' dir exists ", end="")
    sys.stdout.flush()
    try:
        # Getting the list of directories
        toConvdir = os.listdir(toconvp)

        # Checking if the list is empty or not
        if len(toConvdir) == 0:
            time.sleep(0.01)  # fake process
            print("but is empty.")
            print("Be sure to place your video files in the 'ToConvert' dir before running again.  QUITTING.")
            exit()
        else:
            time.sleep(0.01)  # fake process
            print("and contains files.  OK.")
    except OSError as error:
        print(error)
        exit()


# -- conversion actions ///////////////

def zingzing():

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
                    case "gif":
                        CONVCMD = genericC
                    case "webm":
                        CONVCMD = genericC
                    case "mkv":
                        CONVCMD = genericC
                    case "MTS":
                        CONVCMD = genericC
                    case "mpeg":
                        CONVCMD = genericC
                    case _:
                        print("wut duh fuk")

                print(f" {clic.CC202}>>>>{clic.TRESET} {clic.CC2}looking at ......{clic.TRESET} {clic.CC83}{FIF} {clic.TRESET}")
                run(CONVCMD) # , "+"
                print(f" {clic.CC226}>>>>{clic.TRESET} {clic.CC2}new file made ... {clic.CC50}{tohere}{NEWFN}{clic.TRESET}")

        x2mp4(t,FRO,TOO)

    print("All done.  Hopefully it all went well.  Bye!\n")

zingzing()

# --- end //////////////////////////////////////////////////////////////////////

exit()