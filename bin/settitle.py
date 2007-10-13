#!/usr/bin/env python

import glob
import shutil
import sys
import pyid3lib

def read_titles():
    f = open('album.txt')
    artist = f.readline().strip()
    album = f.readline().strip()
    songs = map(str.strip, f.readlines())
    f.close()
    return artist, album, songs

def main():
    mp3s = glob.glob('*.mp3')
    artist, album, songs = read_titles()
    if len(mp3s) != len(songs):
        print >> sys.stderr, "Invalid number of titles"
        sys.exit(1)

    for filename, songname in zip(mp3s, songs):
        tag = pyid3lib.tag(filename)
        tag.album = album
        tag.artist = artist
        tag.title = songname.split(' ', 1)[1] # remove the number in front
        tag.update()
        shutil.move(filename, songname + '.mp3')

if __name__ == '__main__':
    main()
