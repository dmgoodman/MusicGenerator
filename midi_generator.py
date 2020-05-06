import pretty_midi
import json
import os

def json_to_notes_list(json_file):
    file = open(json_file, "r")
    data = json.load(file)
    return data['notes']

def main():
    generated_path = os.getcwd() + '/midi_generated'
    for file in os.listdir('midi_generated'):
        if file.endswith('.json'):
            midi_obj = pretty_midi.PrettyMIDI()
            piano_program = pretty_midi.instrument_name_to_program('Electric Piano 1')
            piano = pretty_midi.Instrument(program = piano_program)
            s = 0
            e = 0.2
            notes_list = json_to_notes_list(generated_path + '/' + file)
            for chord in notes_list:
                if chord:
                    for note in chord:
                        note = pretty_midi.Note(velocity = 60, pitch = note, start = s, end = e)
                        piano.notes.append(note)
                s += 0.2
                e += 0.2

            midi_obj.instruments.append(piano)
            midi_obj.write(generated_path + '/' + file[:-5] + '.mid')

if __name__ == "__main__":
    main()