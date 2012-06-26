#!/usr/bin/python2.7

import os,ConfigParser
from mplayer import Player, CmdPrefix
from random import randint
from time import sleep


conf = ConfigParser.SafeConfigParser()
conf.read('alarm.conf')

music = conf.get('player','music_dir')
randomize = conf.getboolean('player','randomize')
controller = conf.get('player','fifo')
fifo_path = conf.get('player','fifo')

def snooze(player,time=900):
    '''
    Pauses playback for time
    in seconds.
    Time deafult to 900 (15 minutes)
    '''
    player.pause()
    sleep(time)
    player.pause()

def get_songs(music_dir):
    """
    Returns a list of all songs in
    music_dir and subdirectories.
    Songs are in absolute path format
    """
    songs = []
    for entry in os.walk(music_dir):
        for song in entry[2]:
            songs.append(os.path.join(entry[0],song))
    return songs

def start_playback(songs_list,randomize_songs):
    """
    Initalizes the player and begins playback.
    Player must be assigned else it's garbage collected.
    """

    Player.cmd_prefix = CmdPrefix.PAUSING_KEEP
    player = Player()
    
    if randomize_songs:
        rand_song= randint(0,len(songs_list)-1)
        player.loadfile(songs_list[rand_song])
    else:
        player.loadfile(songs_list[0])
    
    return player

def create_fifo(path):
    '''
    Creates the fifo. Deleting the old one
    if it exist.
    '''

    try:
        os.mkfifo(path)
    except OSError:
        #Fifo already exists
        os.unlink(path)
        os.mkfifo(path)
        print "Flushed"


def run():
    """
    Grabs songs, begins playback and
    creates the command fifo.
    Reads from the fifo until it catches 
    "quit" or "snooze <time>"
    """
    

    songs = get_songs(music)
    player = start_playback(songs,randomize)
    
    create_fifo(fifo_path)
    fifo = open(fifo_path)

    while True:
        #Reads command from fifo, strips trailing 
        #newline and splits to list.
        command = fifo.read().strip().split(" ")
        if command[0] == "quit":
            quit(player)
            break
        elif command[0] == "snooze":
            try:
                time = int(command[1])
                snooze(player,time)
            except:
                snooze(player)

    return player

def quit(player):
    os.unlink(fifo_path)
    player.quit()

p = run()

