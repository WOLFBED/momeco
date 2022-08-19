#!/usr/bin/env python

# --- by WOLFBED (c) 2022

# --- notes ////////////////////////////////////////////////////////////////////////////////////////////////////////////
"""

momeco.cuda.cli.py : MOtion MEdia COnverter - CLI version, accepts arguments
                     (cuda edition)

---------

1. place files to convert in ToConvert/ dir
2. run $ momeco.cuda.cli.py [fromHere] [encoder] [preset] [tune]
3. converted files will materialize in fromHere/momeco_done/ dir

NB : - currently only converts to mp4
     - currently only converts from gif, webm, mkv, mts, mpeg

---------

REQUIRES: - python
          - ffmpeg

"""
# --- imports //////////////////////////////////////////////////////////////////////////////////////////////////////////

import shell_colors as clic
from sys import exit, argv
from subprocess import run
from os import popen
import os
import argparse

# --- ~statics /////////////////////////////////////////////////////////////////////////////////////////////////////////

thisScript = "momeco.cuda.cli.py"
outputSubdir = "momeco_done"

genericMeSage = ' >>> missing or invalid argument(s) ...\n'
dirMeSage = " >>> invalid path: '{}' ...\n"
encoderMeSage = " >>> invalid encoder: '{}' ...\n"
tuneMeSage = " >>> invalid tune: '{}' ...\n"

meSage = '   USAGE: {} [dir] [encoder] [preset] [tune] [-mp42]\n      dir: directory where the videos to convert are\n           the converted videos go in dir/momeco_done/\n           if there\'s spaces in the path, put it in quotes, e.g.: "/my/path name/is/this"\n      encoder: h264, h265\n      preset: veryslow, slower, slow, medium (default), fast, faster, veryfast, superfast, ultrafast\n      tune: film, animation, grain, stillimage, fastdecode, zerolatency\n      -mp42: also convert files are already mp4.  if this argument excluded, mp4 are ignored'

# other
TYPES2DO = ["gif", "webm", "mkv", "MTS", "mpeg"]

# --- check arguments //////////////////////////////////////////////////////////////////////////////////////////////////

parser = argparse.ArgumentParser(description='convert video files from one format to mp4')

parser.add_argument("inputDir", help="input directory path")
parser.add_argument("encoder", help="h264 or h265")
parser.add_argument("preset", help="veryslow, slower, slow, medium (default), fast, faster, veryfast, superfast, ultrafast")
parser.add_argument("tune", help="film, animation, grain, stillimage, fastdecode, zerolatency")
parser.add_argument("-mp42", help="also converts files that are already mp4.   if this argument is excluded, .mp4's are ignored")

args = parser.parse_args()
if args.verbosity:
    print("also converts files that are already mp4.   if this argument is excluded, .mp4's are ignored")



try:
    fromHere = argv[1]
except:
    print(meSage.format(thisScript))
    print(" >> QUITTING")
    exit()

try: encoder = argv[2]
except:
    print(meSage.format(thisScript))
    print(" >> QUITTING")
    exit()

try: preset = argv[3]
except:
    print(meSage.format(thisScript))
    print(" >> QUITTING")
    exit()

try:
    tune = argv[4]
    if tune != "-mp42":
        tune = tune
    if tune == "-mp42":
        mp42Q = True
except:
    print(" >>> tune argument is missing ...")
    tune = None
    print(meSage.format(thisScript))
    dwing = input(" >> continue nonetheless?  [Y/n]: ")
    match dwing:
        case "Y" | "y" | "Yes" | "yes" | "yeah" | "Yeah" | "yay" | "Yay":
            noTune = True
        case "N" | "n" | "No" | "no" | "nay" | "Nay" | "Nah" | "nah" | "naw" | "Naw":
            print("ok, so, no.  QUITTING")
            exit()
        case _:
            print("    assuming yes.  continuing without -tune settings")
            noTune = True

try:
    premp42Q = argv[5]
    match premp42Q:
        case "-mp42":
            mp42Q = True
        case "":
            mp42Q = False
        case _:
            mp42Q = False
except:
    # print(" >>> tune argument is missing ...")
    mp42Q = None

# --- check argument data //////////////////////////////////////////////////////////////////////////////////////////////

# check that input dir is good
fromHere =  os.path.normpath(fromHere)
inputPathIsReal = os.path.exists(fromHere)
if inputPathIsReal is not True:
    print(dirMeSage.format(fromHere)+meSage.format(thisScript))
    exit()

# check that output dir exists, if not ask to create
toHere = os.path.normpath(fromHere+"/"+outputSubdir)
outputPathIsReal = os.path.exists(toHere)
if outputPathIsReal is not True:
    jaOrWa = input(f" >>> output path '{toHere}' doesn't exist.  create?  [Y/n]: ")
    match jaOrWa:
        case "Y" | "y" | "Yes" | "yes" | "yeah" | "Yeah" | "yay" | "Yay":
            # create dir
            try:
                os.mkdir(toHere)
            except:
                print(" >>>> couldn't create output dir for some reason.  make sure permissions are ok in the input dir.  QUITTING")
                exit()
            print(" >> done.  moving on ...")
        case "N" | "n" | "No" | "no" | "nay" | "Nay" | "Nah" | "nah" | "naw" | "Naw":
            print("ok, so, no.  QUITTING")
            exit()
        case _:
            print("assuming no.  so, no.  QUITTING")
            exit()

# check codec
match encoder:
    case "h265":
        ReCo = "hevc_nvenc"
    case "h264":
        ReCo = "h264"
    case _:
        print(encoderMeSage.format(encoder) + meSage.format(thisScript))
        exit()

# check preset
match preset:
    case "veryslow":
        preset = "veryslow"
    case "slower":
        preset = "slower"
    case "medium":
        preset = "medium"
    case "fast":
        preset = "fast"
    case "veryfast":
        preset = "veryfast"
    case "superfast":
        preset = "superfast"
    case "ultrafast":
        preset = "ultrafast"
    case _:
        print(" >>> invalid preset '" + preset + "'.  defaulting to 'medium'")
        preset = "medium"

# check tune
if tune:
    match tune:
        case "film":
            tune = "film"
        case "animation":
            tune = "animation"
        case "grain":
            tune = "grain"
        case "stillimage":
            tune = "stillimage"
        case "fastdecode":
            tune = "fastdecode"
        case "zerolatency":
            tune = "zerolatency"
        case "-mp42":
            mp42Q = True
        case _:
            print(" >>> invalid tune '"+tune+"'.  defaulting to 'fastdecode'")
            tune = "fastdecode"

# --- ~semi-statics ////////////////////////////////////////////////////////////////////////////////////////////////////

# paths
# from...
if fromHere[:-1] == "/":
    fromHere = fromHere.replace(fromHere[:-1],"")
FRO = fromHere
# to...
TOO = f"{FRO}/momeco_done"

# ask to delete original files after successful conversion
convQ = input(" >>>> delete original files after conversion?  [y/N]: ")

toConvert = []
converted = []


# --- actions //////////////////////////////////////////////////////////////////////////////////////////////////////////

for t in TYPES2DO:

    def x2mp4(ext,fromhere,tohere) :

        FIFS = popen(f'find {fromhere} -name "*.{ext}"', "r").readlines()

        FIFFERS = []

        for f in FIFS :
            coif = f.replace("\n","").replace("./","")
            FIFFERS.append(coif)

        for FIF in FIFFERS:

            toConvert.append(FIF)

            NEWFN = FIF.replace(f".{ext}", ".mp4").replace(f"{fromhere}","")

            CONVCMD = []

            # full conversion commands, one with and the other without -tune settings
            if noTune is not True:
                genericC = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-hwaccel", "cuda", "-i", f"{FIF}", "-c:v", f"{encoder}", "-preset", f"{preset}", "-tune", f"{tune}", "-f", "mp4", f"{tohere}{NEWFN}"]
            elif noTune is True:
                genericC = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-hwaccel", "cuda", "-i", f"{FIF}", "-c:v", f"{encoder}", "-preset", f"{preset}", "-f", "mp4", f"{tohere}{NEWFN}"]


            # determine if input file extension is actionable, I know this sucks and should be based on codec of the stream, but for now ...
            if mp42Q == False | None:
                match ext:
                    case "gif" | "webm" | "mkv" | "MTS" | "mpeg" : CONVCMD = genericC
                    case _:
                        print("extension not actionable")
            elif mp42Q == True:
                match ext:
                    case "mp4" | "gif" | "webm" | "mkv" | "MTS" | "mpeg":
                        CONVCMD = genericC
                    case _:
                        print("extension not actionable")

            print(f" {clic.CC202}>>>>{clic.TRESET} {clic.CC2}looking at ......{clic.TRESET} {clic.CC83}{FIF} {clic.TRESET}")

            try:
                run(CONVCMD) # , "+"
                converted.append(f"{tohere}{NEWFN}")
            except:
                print(" >>> couldn't convert video(s) for some reason.  fuck this, QUITTING")
                exit()
            print(f" {clic.CC226}>>>>{clic.TRESET} {clic.CC2}new file made ... {clic.CC50}{tohere}{NEWFN}{clic.TRESET}")

    x2mp4(t,FRO,TOO)

print("All done.  Hopefully it all went well.  Bye!\n")

print("files to convert: " + str(toConvert))
print("\nfiles that have been converted: " + str(converted))

# --- end //////////////////////////////////////////////////////////////////////////////////////////////////////////////

exit()