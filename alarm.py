#!/usr/bin/python2.7

import os,argparse,ConfigParser 
from mplayer import Player, CmdPrefix

conf_loc = os.path.expanduser("~/.config/alarm/alarm.conf")
conf = ConfigParser.SafeConfigParser()
conf.read(conf_loc)

working_dir = conf.get('player','working_dir')

def set_alarm(args):
    """
    Calls atd to run play_alarm at the time specified by set.
    You should read the manual for at, but "7:00AM" is pretty 
    self-explanatory.
    """
    
    #echo "/home/user/scripts/play_alarm.py" | at 7:00AM
    command ="echo \" "+os.path.join(working_dir,"play_alarm.py")+"\" |  at "+args.time
    os.system(command)


def stop_alarm(args):
    """
    Sends a "quit" command to the alarm.
    """
    fifo = open(os.path.join(working_dir,"command.fifo"),'w')
    fifo.write("quit")
    fifo.close()

def snooze_alarm(args):
    """
    Pauses the alarm for given minutes then resumes playback.
    """
    fifo = open(os.path.join(working_dir,"command.fifo"),'w')
    fifo.write("snooze "+args.minutes)

def play_alarm(args):
    os.system(os.path.join(working_dir,"play_alarm.py"))

#Top level parser
parser = argparse.ArgumentParser(description="Set and manage an alarm")
subparsers = parser.add_subparsers()

#Time parser
time_parser = subparsers.add_parser("set",help = "Set the alarm")
time_parser.add_argument('time',help="The time to play the alarm")
time_parser.set_defaults(func=set_alarm)

#Play parser
play_parser = subparsers.add_parser("play",help="Play alarm")
play_parser.set_defaults(func=play_alarm)

#Stop parser
stop_parser = subparsers.add_parser("stop",help="Stop alarm playback")
stop_parser.set_defaults(func=stop_alarm)

#Snooze parser
snooze_parser = subparsers.add_parser("snooze",help="Snooze the alarm")
snooze_parser.add_argument('minutes',help="Minutes to snooze.")
snooze_parser.set_defaults(func=snooze_alarm)

args = parser.parse_args()
args.func(args)
