#!/usr/bin/python3

import subprocess
import os
import sys
import json
from time import sleep

def readConfig(configFile):
    settingsFile = os.path.join(cwd, configFile)
    with open(settingsFile) as json_file:
        data = json.load(json_file)
    return data

def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches

audioFiles = ["Amarelo_Vermelho.wav", "Azul_Verde.wav"]

# Get the current working 
# directory (CWD)
try:
    this_file = __file__
except NameError:
    this_file = sys.argv[0]
this_file = os.path.abspath(this_file)
if getattr(sys, 'frozen', False):
    cwd = os.path.dirname(sys.executable)
else:
    cwd = os.path.dirname(this_file)

# Read Config File
config = readConfig("config.json")
mpvPlayer = cwd + config["mpvPlayer"]
video = cwd + config["video"]
audios = config["audios"]
channels = config["channels"]

for i in range(len(audios)):
    audios[i] = cwd + audios[i]

# Get device list to specify output channels
str = subprocess.check_output([mpvPlayer, "--audio-device=help"]).decode("utf-8")
device = ""
deviceList = []
for i in str:
    device = device + i
    if i == "\n":
        deviceList.append(device)
        #print(device)
        device = ""
    
#print (deviceList)
wasapi = []
i = 0
for new in deviceList:
    if channels[i] in new:
        getDevice = list(find_all(new, "'"))
        subprocess.Popen([mpvPlayer, f"--audio-device={new[getDevice[0]+1: getDevice[1]]}", "--loop-playlist", audios[i]])
        print(f"playing audio {i}")
        i =+ 1
#sleep(1)
#play video in loop
subprocess.Popen([mpvPlayer, "--loop-playlist", "--fullscreen", "--no-osc", "--ontop", video], stdin=subprocess.PIPE)

print("playing video")
