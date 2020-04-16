import os
import sys
import mido
from mido import MidiFile

cwd_new = os.getcwd() + "/midi_audio_train"
for midifile in os.listdir(cwd_new):
    path = "{}/{}".format(cwd_new, midifile)
    with open("{}/midi_train/{}.txt".format(os.getcwd(), midifile), "w") as output:
        mid = MidiFile(path)
        for track in mid.tracks:
            for msg in track:
                # store event type followed by attributes
                if not msg.is_meta:
                    msg = str(msg)
                    event = msg.split()
                    line = ""
                    for i, attribute in enumerate(event):
                        if i == 0:
                            attribute = event[i]
                            line += attribute + " "
                        else:
                            attribute = event[i].split("=")[1]
                            line += attribute + " "
                    output.write(line + "\n")
                    
                # store metadata such as tempo, track name, etc.
                else:
                    output.write(str(msg) + "\n")
