import os
import pretty_midi

cwd_new = os.getcwd() + "/midi_audio"
for midifile in os.listdir(cwd_new):
    path = "{}/{}".format(cwd_new, midifile)
    with open("{}/midi_processed/{}.txt".format(os.getcwd(), midifile[:-4]), "w") as output:
        midi_data = pretty_midi.PrettyMIDI(path)
        midi_dict = {}
        for instrument in midi_data.instruments:
            for note in instrument.notes:
                start = note.start
                end = note.end
                pitch = note.pitch
                #velocity = note.velocity
                midi_dict[(start, end)] = midi_dict.get((start, end), [])
                midi_dict[(start, end)].append(pitch)
            midi_list = sorted(midi_dict.items(), key = lambda key: key[0])
            for item in midi_list:
                output.write(str(item[0]) + " " + str(item[1]) + "\n")