import random
import json
import os

#---------------------------------------------------------------------

def preprocess_firstorder(notes_list):
    notesDict = {}
    for i in range(len(notes_list)):
        notes = tuple(notes_list[i])
        prevNotes = tuple([])
        if i > 0:
            prevNotes = tuple(notes_list[i - 1])

        # Set notesDict[prevNotes] to empty dictionary if it doesn't exist
        notesDict[prevNotes] = notesDict.get(prevNotes, {})

        # Set notesDict[prevNotes][notes] to 1 if it doesn't exist
        notesDict[prevNotes][notes] = notesDict[prevNotes].get(notes, 0) + 1

    return notesDict

#---------------------------------------------------------------------

def preprocess(notes_list, order):
    notesDict = {}
    for i in range(len(notes_list)):
        workingDict = notesDict
        for j in range(order):
            if j < order - 1:
                current_notes = tuple(notes_list[i - (order - j)]) if i - (order - j) >= 0 else tuple([])
                workingDict[current_notes] = workingDict.get(current_notes, {})
            else:
                current_notes = tuple(notes_list[i - (order - j)]) if i - (order - j) >= 0 else tuple([])
                workingDict[current_notes] = workingDict.get(current_notes, 0) + 1
            workingDict = workingDict[current_notes]

    return notesDict

#---------------------------------------------------------------------

def get_order(markov_dict):
    order = 0
    while type(markov_dict) is not int:
        markov_dict = markov_dict[()]
        order += 1
    return order

#---------------------------------------------------------------------

def generate(markov_dict, num_notes):
    order = get_order(markov_dict)
    
    notes = []
    for i in range(order - 1):
        notes.append(())

    for i in range(num_notes):
        working_dict = markov_dict
        for j in range(order - 1):
            working_dict = working_dict[notes[i + j]]
            
        total = 0
        for key in working_dict:
            total += working_dict[key]
        seed = random.randint(0, total - 1)

        total = 0
        for key in working_dict:
            total += working_dict[key]
            if seed < total:
                notes.append(key)
                break

    return notes

#---------------------------------------------------------------------

def json_to_notes_list(json_file):
    file = open(json_file, "r")
    data = json.load(file)
    return data['notes']

#---------------------------------------------------------------------

def generate_from_json_files(json_files, order, num_notes):
    full_notes_list = []
    
    for file in json_files:
        notes_list = json_to_notes_list(file)
        for notes in notes_list:
            full_notes_list.append(notes)

    notes_dict = preprocess(full_notes_list, order)
    notes = generate(notes_dict, num_notes)

    return notes

def generate_from_directory(directory, order, num_notes):
    json_files = []
    for file in os.listdir(directory):
        if file.endswith('.json'):
            json_files.append(directory + '/' + file)
    return generate_from_json_files(json_files, order, num_notes)

#---------------------------------------------------------------------

def main():
    notes = generate_from_directory('midi_discretized', 3, 10000)
    print(notes)

#---------------------------------------------------------------------

if __name__ == "__main__":
    main()
