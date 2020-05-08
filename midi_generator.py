import pretty_midi
import json
import os
import sys

def json_to_notes_list(json_file, default_interval):
    with open(json_file, "r") as file:
        data = json.load(file)
        # hack because cant figure out the 2x oddity atm
        return data.get('increment', default_interval) / 2.0, data['notes']

def main(default_interval):
    generated_path = os.getcwd() + '/midi_generated'
    for file in os.listdir('midi_generated'):
        if file.endswith('.json'):
            midi_obj = pretty_midi.PrettyMIDI()
            piano_program = pretty_midi.instrument_name_to_program('Electric Piano 1')
            piano = pretty_midi.Instrument(program=piano_program)

            increment, notes_list = json_to_notes_list(generated_path + '/' + file, default_interval)
            curr_time = 0.0
            curr_notes = {}
            for chord in notes_list:
                ending_notes = curr_notes.keys() - set(chord)
                for note in ending_notes:
                    pm_note = pretty_midi.Note(velocity=60, pitch=note, start=curr_notes[note], end=curr_time)
                    del curr_notes[note]
                    piano.notes.append(pm_note)
                for note in chord:
                    if curr_notes.get(note) is None:
                        curr_notes[note] = curr_time
                curr_time += increment

            midi_obj.instruments.append(piano)
            midi_obj.write(generated_path + '/' + file[:-5] + '.mid')

if __name__ == "__main__":
    default_interval = float(sys.argv[1]) if len(sys.argv) >= 2 else 0.2
    main(default_interval)
