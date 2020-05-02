import pretty_midi

midi_obj = pretty_midi.PrettyMIDI()
piano_program = pretty_midi.instrument_name_to_program("Electric Piano 1")
piano = pretty_midi.Instrument(program = piano_program)

s = 0
e = 0.5

for note_number in [55, 60, 65, 60, 70]:
    note = pretty_midi.Note(velocity = 60, pitch = note_number, start = s, end = e)
    piano.notes.append(note)
    s += 0.5
    e += 0.5

midi_obj.instruments.append(piano)
# key = pretty_midi.KeySignature(0, 0)
# midi_obj.key_signature_changes(key)
midi_obj.write("test_generated.mid")