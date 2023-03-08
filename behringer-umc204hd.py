#!/usr/bin/python3

import subprocess
import os
import sys

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
mpvPlayer = cwd + "\mpv"
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
for new in deviceList:
    if "OUT 1-2 (" in new:
        getDevice = list(find_all(new, "'"))
        wasapi.append(new[getDevice[0]+1: getDevice[1]])
    if "OUT 3-4 (" in new:
        getDevice = list(find_all(new, "'"))
        wasapi.append(new[getDevice[0]+1: getDevice[1]])
print(wasapi)
i = 0
for audioDevice in wasapi:
    subprocess.Popen([mpvPlayer, f"--audio-device={audioDevice}", "--loop", audioFiles[i]])
    i =+ 1
    
