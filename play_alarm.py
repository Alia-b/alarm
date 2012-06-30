#!/usr/bin/python2.7

import os,ConfigParser
from mplayer import Player, CmdPrefix
from random import randint
from time import sleep


conf_loc = os.path.expanduser("~/.config/alarm/alarm.conf")
conf = ConfigParser.SafeConfigParser()
conf.read(conf_loc)

music = conf.get('player','music_dir')
randomize = conf.getboolean('player','randomize')
working_dir = conf.get('player','working_dir')


def snooze(player,minutes=15):
    '''
    Pauses playback for minutes.
    Defaults to 15 minutes.
    '''
    player.pause()
    #Convert minutes to seconds for sleep()
    sleep(minutes*60)
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
    player = Player('-loop -1')
    
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
    fifo_path = os.path.join(path,"command.fifo")
    if os.path.exists(fifo_path):
        os.unlink(fifo_path)
    os.mkfifo(fifo_path)
    return fifo_path

def run():
    """
    Grabs songs, begins playback and
    creates the command fifo.
    Reads from the fifo until it catches 
    "quit" or "snooze <time>"
    """
    

    songs = get_songs(music)
    player = start_playback(songs,randomize)
    
    fifo_loc =  create_fifo(working_dir)
    fifo = open(fifo_loc)

    while True:
        #Reads command from fifo, strips trailing 
        #newline and splits to list.
        command = fifo.read().strip().split(" ")
        if command[0] == "quit":
            quit(player,fifo_loc)
            break
        elif command[0] == "snooze":
            try:
                time = int(command[1])
                snooze(player,time)
            except:
                snooze(player)

    return player

def quit(player,fifo_path):
    os.unlink(fifo_path)
    player.quit()

p = run()

