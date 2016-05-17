#!/usr/bin/python

import os
import shutil
from tinytag import TinyTag
import argparse
import fnmatch

parser = argparse.ArgumentParser()

parser.add_argument("--verbosity", default=0, help="increase output verbosity", type=int)
parser.add_argument("--destination", help="Destination Path")
parser.add_argument("--source", help="Source Path")

args = parser.parse_args()

dest = args.destination
src = args.source

if not os.path.exists(src):
    sys.stderr("source path does not exists!!!")

if not os.path.exists(dest):
    os.mkdir(dest)
    if args.verbosity > 1:
            print("create destination")

mp3files = []

for root, dirs, files in os.walk(src):

    for name in fnmatch.filter(files, "*.mp3"):
        mp3files.append(os.path.join(root, name))

        if args.verbosity:
            print(os.path.join(root, name))

if len(mp3files) == 0:
    sys.stderr("Error no mp3 file!")

for mp3file in mp3files:
    
    if args.verbosity > 1:
        print('mp3 file path %s' % mp3file)

    tag = TinyTag.get(mp3file)

    if args.verbosity > 0:
        print('This track is by %s.' % tag.artist)
        print('It is %f seconds long.' % tag.duration)

    artpath = os.path.join(dest, tag.artist)
    albpath = os.path.join(artpath, tag.album)

    if not os.path.exists(artpath):
        os.mkdir(artpath)
        if args.verbosity > 1:
            print(artpath)
        if not os.path.exists(albpath):
            os.mkdir(albpath)
            if args.verbosity > 1:
                print(albpath)
        else:
            if not os.path.exists(albpath):
                os.mkdir(albpath)
                if args.verbosity > 1:
                    print(albpath)

    if args.verbosity > 0:
        print("MP3 File is %s" % mp3file)
        print("Move to %s" % albpath+"/"+os.path.basename(mp3file))

    shutil.move(mp3file, albpath+"/"+os.path.basename(mp3file))
