#!/usr/bin/python2.7

import os,wx 
from mplayer import Player, CmdPrefix

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

def start_playback(song):
    Player.cmd_prefix = CmdPrefix.PAUSING_KEEP
    player = Player()
    player.loadfile(song)

    return player

songs = get_songs(music)
foo = start_playback(songs[1])

app = wx.App()
frame = wx.Frame(None,-1,"Alarm")
frame.Show()
app.MainLoop()




