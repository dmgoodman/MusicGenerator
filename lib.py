import json

from collections import namedtuple

TimeInterval = namedtuple('TimeInterval', ['start', 'end'])
NoteInterval = namedtuple('NoteInterval', ['interval', 'notes'])


def note_interval(fileptr):
    data = json.load(fileptr)
    for item in data:
        yield NoteInterval(
            TimeInterval(item['start'], item['end']),
            item['notes'],
        )


def note_interval_list(fileptr):
    return list(note_interval(fileptr))
