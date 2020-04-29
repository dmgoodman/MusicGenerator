import os
import mido
from mido import MidiFile

cwd_new = os.getcwd() + "/midi_audio"
for midifile in os.listdir(cwd_new):
    path = "{}/{}".format(cwd_new, midifile)
    with open("{}/midi_messages/{}.txt".format(os.getcwd(), midifile), "w") as output:
        mid = MidiFile(path)
        for track in mid.tracks:
            for msg in track:
                output.write(str(msg) + "\n")