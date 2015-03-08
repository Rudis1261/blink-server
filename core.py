#!/bin/python
import os
import time
import subprocess
import commands
import json

# Change the PWD to this locationself.wfile.write(
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Variables (Constants)
DEFAULT_VIDEO = 'totem'
DEFAULT_MUSIC = 'rhythmbox'
APPS = ('totem', 'vlc', 'xbmc', 'rhythmbox')

def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError, e:
        return False
    return True

# Kill all running aps
def killApps():

    # Loop through them and kill them as we go along
    for APP in APPS:
        getPid = commands.getoutput("ps -e | grep " + APP + " | awk {'print $1'}")
        #print "ps -e | grep " + APP + " | awk {'print $1'} , PID: " + getPid

        # If there is a PID, then the application is running and we can kill it
        if getPid != '':
            commands.getoutput('kill ' + getPid)
            print 'Killing ' + APP + ", VIA: " + 'kill ' + getPid

# This function will be used to confirm whether an application is running
def appRunning(APP):

    # Get the PID, if it exists then the app is running
    getPid = commands.getoutput("ps -e | grep " + APP + " | awk {'print $1'}")

    # If there is a PID, then the application is indeed running
    if getPid != '':
        return False
    else:
        return True

# This will perform the actions
def commandKeys(pressed):

    # The dictionary with the commands and switches to be run
    defaults = {
        'up':       ['xdotool', 'key', "Up"],
        'down':     ['xdotool', 'key', "Down"],
        'left':     ['xdotool', 'key', "Left"],
        'right':    ['xdotool', 'key', "Right"],
        'ok':       ['xdotool', 'key', "KP_Enter"],
        'play':     ['xdotool', 'key', "XF86AudioPlay"],
        'info':     ['xdotool', 'key', 'Menu'],
        'back':     ['xdotool', 'key', "Escape"],
        'next':     ['xdotool', 'key', "XF86AudioNext"],
        'prev':     ['xdotool', 'key', "XF86AudioPrev"],
        'video':    [DEFAULT_VIDEO],
        'stop':     ['xdotool', 'key', "XF86AudioStop"],
        'music':    [DEFAULT_MUSIC],
        'vol-up':   ['xdotool', 'key', "XF86AudioRaiseVolume"],
        'vol-down': ['xdotool', 'key', "XF86AudioLowerVolume"],
        'click' :   ['xdotool', 'click', "1"],
        'rclick' :  ['xdotool', 'click', "3"]
    }

    # Did we receive a JSON string?
    if is_json(pressed):
        JSON = json.loads(pressed)

        # Currently we are only concerned with moving the mouse
        if JSON['action'] == "mouse-move":

            # Handle negative values
            if JSON['x'] < 0 or JSON['y'] < 0:
                mouseCommand = [
                    'xdotool',
                    'mousemove_relative',
                    '--',
                    str(JSON['x']),
                    str(JSON['y'])
                ]
            else:
                mouseCommand = [
                    'xdotool',
                    'mousemove_relative',
                    str(JSON['x']),
                    str(JSON['y'])
                ]

            # Dispatch the mouse move event
            xdotool(mouseCommand)


    # Was the keypress valid? If so, run the relevant command
    elif pressed == "power":
        killApps()

    elif pressed == "fullscreen":
        xdotool(defaults['click'], True)
        xdotool(defaults['click'], True)

    # The media launchers are a bit different, we need to check that the application is not already fired up
    elif pressed == "video" or pressed == "music":

        # Check if it's already running, if not kill all other players listed in apps and open this one
        if appRunning(str(defaults[pressed])) == False:
            #killApps()
            appLaunch(defaults[pressed], True)
            print "Launching " + str(defaults[pressed])
        else:
            print str(defaults[pressed]) + " is already running"

    # Othewise lets check the action to be run, based on the key pressed
    elif pressed in defaults:
        print defaults[pressed]
        xdotool(defaults[pressed])

    # Command not found sadly
    else:
        print pressed, "command not found, Eish"

# This little baby is what sends the command from the dictionary to the kernel to be processed.
def xdotool(action, surpress=False):
    ps = subprocess.Popen(action)
    if surpress == False:
        print action

# Applications should be done a bit differently
def appLaunch(action, surpress=False):
    FNULL = open('/dev/null', 'w')
    ps = subprocess.Popen(action, shell=True, stderr=FNULL)
    if surpress == False:
        print action