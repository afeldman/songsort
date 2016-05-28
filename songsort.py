#!/usr/bin/python

import os
import shutil
from tinytag import TinyTag
import argparse
import fnmatch
import uuid

parser = argparse.ArgumentParser()

parser.add_argument("--verbosity", default=0, help="increase output verbosity", type=int)
parser.add_argument("--destination", help="Destination Path")
parser.add_argument("--source", help="Source Path")

args = parser.parse_args()

dest = args.destination
src = args.source
vlevel = args.verbosity

if not os.path.exists(src):
    sys.stderr("source path does not exists!!!")

if not os.path.exists(dest):
    os.mkdir(dest)
    if vlevel > 1:
            print("create destination")

mp3files = []

for root, dirs, files in os.walk(src):

    for name in fnmatch.filter(files, "*.mp3"):
        mp3files.append(os.path.join(root, name))
        if vlevel > 1:
            print(os.path.join(root, name))
    for name in fnmatch.filter(files, "*.Mp3"):
        mp3files.append(os.path.join(root, name))
        if vlevel > 1:
            print(os.path.join(root, name))
    for name in fnmatch.filter(files, "*.MP3"):
        mp3files.append(os.path.join(root, name))
        if vlevel > 1:
            print(os.path.join(root, name))
    for name in fnmatch.filter(files, "*.mP3"):
        mp3files.append(os.path.join(root, name))
        if vlevel > 1:
            print(os.path.join(root, name))
    break

if len(mp3files) == 0:
    sys.stderr("Error no mp3 file!")

for mp3file in mp3files:
    
    if vlevel > 1:
        print('mp3 file path %s' % mp3file)

    try:
        tag = TinyTag.get(mp3file)
        
        if vlevel > 2:
            print('This track is by %s.' % tag.artist)
            print('It is %f seconds long.' % tag.duration)# duration of the song in seconds
            print('The album name is %s' % tag.album)         # album as string
            print('Audio offset %f' % tag.audio_offset)  # number of bytes before audio data begins
            print('bitrate %f' % tag.bitrate)       # bitrate in kBits/s
            print('Filesize %f' % tag.filesize)      # file size in bytes
            print('genre %s' % tag.genre)         # genre as string
            print('sample rate %f' % tag.samplerate)    # samples per second
            print('title %s' % tag.title)         # title of the song
            print('track %s' % tag.track)         # track number as string
            print('title %s' % str(tag.track_total))   # total number of tracks as string
            print('year %s' % str(tag.year))          # year or data as string

        if not tag.genre:
            tag.genre = "no genre"

        if not tag.artist:
            tag.artist = "various"

        if not tag.album:
            tag.album = "no album"

        gerpath = os.path.join(dest, tag.genre)
        artpath = os.path.join(gerpath, tag.artist)
        albpath = os.path.join(artpath, tag.album)

        if not os.path.exists(gerpath):
            os.mkdir(gerpath)
            os.mkdir(artpath)
            os.mkdir(albpath)
            if vlevel > 1:
                print(gerpath)
                print(artpath)
                print(albpath)
        
        if not os.path.exists(artpath):
            os.mkdir(artpath)
            os.mkdir(albpath)
            if vlevel > 1:
                print(artpath)
                print(albpath)

        if not os.path.exists(albpath):
            os.mkdir(albpath)
            if vlevel > 1:
                print(albpath)
            
        if vlevel > 0:
            print("MP3 File is %s" % mp3file)
            print("Move to %s" % albpath+"/"+os.path.basename(mp3file))
            
        shutil.move(mp3file, albpath+"/"+os.path.basename(mp3file))

    except:

        albpath = os.path.join(dest, "unsorted")

        if not os.path.exists(albpath+"/"):
            os.mkdir(albpath)

        n = str(uuid.uuid1())

        shutil.move(mp3file, albpath+"/"+n+".mp3")
