import json

from collections import namedtuple

TimeInterval = namedtuple('TimeInterval', ['start', 'end'])
NoteInterval = namedtuple('NoteInterval', ['interval', 'notes'])


def note_intervals(fileptr):
    data = json.load(fileptr)
    for item in data:
        yield NoteInterval(
            TimeInterval(item['start'], item['end']),
            item['notes'],
        )


def note_intervals_list(fileptr):
    return list(note_intervals(fileptr))


def discretized_notes(fileptr):
    data = json.load(fileptr)
    return data['increment'], data['notes']


def generator_of(single_elem):
    yield single_elem
