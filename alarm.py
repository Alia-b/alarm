#!/usr/bin/python2.7

import os,argparse 
from mplayer import Player, CmdPrefix


path_to_script = "/home/bielobog/code/python/alarm/alarm.py"

#Top level parser
parser = argparse.ArgumentParser(description="Set and manage an alarm")
subparsers = parser.add_subparser()

#Time parser
time_parser = subparsers.add_parser("set",help = "Set the alarm")
time_parser.add_argument('time',help="The time to play the alarm")

#Play parser
play_parser = subparser.add_parser("play",help="Play alarm")

#Stop parser
stop_parser = subparser.add_parser("stop",help="Stop the alarm")

args = parser.parse_args()


def set_alarm(script_path,time):
    os.system("echo \" "+script_path+" \" |  at "+time)

if args.time:
    set_alarm(path_to_script,args.time)

def snooze(time,player):
    player.pause()
    wait(time)
    player.play()

music = '/home/bielobog/Music/Singles'

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

def start_playback(songs,random=True):
    Player.cmd_prefix = CmdPrefix.PAUSING_KEEP
    player = Player()
    player.loadfile(song[0])

    return player

def run():
    songs = get_songs(music)
    player = start_playback(songs)

def quit(player):
    player.quit()


