#!/usr/bin/env python3

import json
import heapq

from multiprocessing import Process, JoinableQueue
from pathlib import Path

from pretty_midi import PrettyMIDI
from lib import TimeInterval


class PriorityQueue:
    # smallest first priority queue

    def __init__(self):
        self.heap = []

    def __bool__(self):
        return bool(self.heap)

    def push(self, priority, item):
        heapq.heappush(self.heap, (priority, item))

    def peek(self):
        if not self.heap:
            return None

        priority, item = self.heap[0]
        return item

    def pop(self):
        if not self.heap:
            return None

        priority, item = heapq.heappop(self.heap)
        return item

    # If the mutiple items are tied for smallest priority, then pop them all.
    def pop_multiple(self):
        if not self.heap:
            return []

        priority, item = heapq.heappop(self.heap)
        result = [item]
        while self.heap and self.heap[0][0] == priority:
            result.append(self.pop())

        return result


def fix_overlap(midi_dict):
    # treats this like a line horizontal line intersection problem

    result = {}
    startpq = PriorityQueue()
    endpq = PriorityQueue()

    for interval, notes in midi_dict.items():
        startpq.push(interval.start, (interval, notes))

    curr_notes = set()
    start_curr_interval = 0.0
    while startpq or endpq:
        startpq_peek, endpq_peek = startpq.peek(), endpq.peek()
        # process endpq.end if before startpq.start or equal
        if ((endpq_peek and startpq_peek and endpq_peek[0].end <= startpq_peek[0].start)
                or (endpq_peek and not startpq_peek)):

            old_notes = curr_notes.copy()
            for interval, notes in endpq.pop_multiple():
                curr_notes -= notes  # set difference

            if old_notes != curr_notes:
                interval, _ = endpq_peek
                if start_curr_interval < interval.end:
                    new_interval = TimeInterval(start_curr_interval, interval.end)
                    result[new_interval] = list(old_notes)

                start_curr_interval = interval.end

        else:
            old_notes = curr_notes.copy()
            for interval, notes in startpq.pop_multiple():
                endpq.push(interval.end, (interval, notes))
                curr_notes |= notes  # set union

            if old_notes != curr_notes:
                interval, _ = startpq_peek
                if start_curr_interval < interval.start:
                    new_interval = TimeInterval(start_curr_interval, interval.start)
                    result[new_interval] = list(old_notes)

                start_curr_interval = interval.start

    return result


def preprocess(midi_path, output_path):
    with midi_path.open('rb') as midi_file, output_path.open('w') as output_file:
        midi_data = PrettyMIDI(midi_file)
        midi_dict = {}
        for instrument in midi_data.instruments:
            for note in instrument.notes:
                start = note.start
                end = note.end
                pitch = note.pitch
                # velocity = note.velocity
                tm = TimeInterval(start, end)
                midi_dict[tm] = midi_dict.get(tm, set())
                midi_dict[tm].add(pitch)

        midi_dict = fix_overlap(midi_dict)
        midi_list = sorted(midi_dict.items())

        json_list = [{
            'start': interval.start,
            'end': interval.end,
            'notes': sorted(notes),
        } for interval, notes in midi_list]
        json.dump(json_list, output_file, indent=2)


def preprocess_worker(file_q):
    while True:
        item = file_q.get()
        if item is None:
            break
        midi_path, output_path = item

        preprocess(midi_path, output_path)
        file_q.task_done()


def main(audio_dir=Path('./midi_audio'), num_workers=10):
    file_q = JoinableQueue()

    # start worker processes
    processes = []
    for i in range(num_workers):
        p = Process(target=preprocess_worker, args=(file_q,))
        p.start()
        processes.append(p)

    # put midi files (and output files) on to file queue
    processed_dir = audio_dir.parent / 'midi_processed'
    if not processed_dir.exists():
        processed_dir.mkdir()
    for midi_path in audio_dir.glob('**/*.mid'):
        output_path = (processed_dir / midi_path.stem).with_suffix('.json')
        file_q.put((midi_path, output_path))

    # block until all files done
    file_q.join()

    # stop workers
    for i in range(num_workers):
        file_q.put(None)
    for p in processes:
        p.join()


if __name__ == '__main__':
    main()
