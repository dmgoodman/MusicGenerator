import random

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

        print("LOP " + str(working_dict))
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

def main():
    notes = [ [1],[2],[3],[4],[1],[4],[2],[2],[3],[4],[1],[4],[2],[2],[3],[4],[1],[4],[2],
              [1],[1],[1],[1],[2],[3],[4],[1],[4],[2],[2],[3],[4],[1],[4],[2],[2],[3],[4],
              [1],[4],[2],[1],[1] ]
    return [preprocess(notes, 1), preprocess(notes, 2), preprocess(notes, 3), preprocess(notes, 4)]
