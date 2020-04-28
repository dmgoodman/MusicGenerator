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

def preprocess(notes_list, order):
    notesDict = {}
    for i in range(len(notes_list)):
        workingDict = notesDict
        for j in range(order):
            if j < order - 1:
                current_notes = tuple(notes_list[i - (order - j)]) if i - (order - j) >= 0 else tuple([])
                workingDict[current_notes] = workingDict.get(current_notes, {})
                print(current_notes, end="")
            else:
                current_notes = tuple(notes_list[i - (order - j)]) if i - (order - j) >= 0 else tuple([])
                workingDict[current_notes] = workingDict.get(current_notes, 0) + 1
                print(current_notes)
            workingDict = workingDict[current_notes]

    return notesDict

def main():
    notes = [ [1],[2],[3],[4],[1],[4],[2],[2],[3],[4],[1],[4],[2],[2],[3],[4],[1],[4],[2],
              [1],[1],[1],[1],[2],[3],[4],[1],[4],[2],[2],[3],[4],[1],[4],[2],[2],[3],[4],
              [1],[4],[2],[1],[1] ]
    return [preprocess(notes, 1), preprocess(notes, 2), preprocess(notes, 3), preprocess(notes, 4)]
