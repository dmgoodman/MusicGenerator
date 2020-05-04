#!/usr/bin/env python3

import json
import math
import sys

from multiprocessing import Process, JoinableQueue
from pathlib import Path

from lib import note_intervals, generator_of


def discretize(input_path, output_path, increment, debug):
    with input_path.open('rb') as input_file, output_path.open('w') as output_file:
        # find smallest interval length for increment if necessary
        if increment is None:
            increment = min((intv.end - intv.start
                            for intv, _ in note_intervals(input_file)))
            input_file.seek(0)

        # discretize
        if debug:
            length_deltas = []
        output = []
        start = 0.0
        for interval, notes in note_intervals(input_file):
            int_length = interval.end - start
            inc_count = round(int_length / increment)
            output.extend([notes] * inc_count)

            if debug:
                new_end = start + inc_count * increment
                length_delta = new_end - start - interval.end + interval.start
                length_deltas.append(length_delta)
                print('{} {} Length Delta: {}'.format(
                    (round(start, 10), round(new_end, 10)),
                    notes,
                    round(length_delta, 10),
                ), file=sys.stderr)

            start += inc_count * increment

        if debug:
            print('Mean Length Delta:',
                  round(math.fsum(length_deltas) / len(length_deltas), 10),
                  file=sys.stderr)

        # dump result
        json.dump({'increment': increment, 'notes': output}, output_file)


def discretize_worker(file_q, increment, debug):
    while True:
        item = file_q.get()
        if item is None:
            break
        input_path, output_path = item

        discretize(input_path, output_path, increment, debug)
        file_q.task_done()


def main(increment, debug, processed_dir=Path('./midi_processed'), num_workers=10):
    file_q = JoinableQueue()

    # start worker processes
    processes = []
    for i in range(num_workers):
        p = Process(target=discretize_worker, args=(file_q, increment, bool(debug)))
        p.start()
        processes.append(p)

    # put input processed files (and output files) on to file queue
    discretized_dir = processed_dir.parent / 'midi_discretized'
    if not discretized_dir.exists():
        discretized_dir.mkdir()

    input_file_generator = (generator_of(processed_dir / debug) if debug
                            else processed_dir.glob('**/*.json'))
    for input_path in input_file_generator:
        output_path = discretized_dir / input_path.name
        file_q.put((input_path, output_path))

    # block until all files done
    file_q.join()

    # stop workers
    for i in range(num_workers):
        file_q.put(None)
    for p in processes:
        p.join()


if __name__ == '__main__':
    # Usage: (debug should be a filename, increment should be float)
    #   ./midi_discretizer.py [debug] [increment]
    # If increment is not present, smallest note time interval is used.
    # If debug is present, just that file is discritized and extra output is
    # produced. Debug is relative to ./midi_processed.
    increment, debug = None, None
    if len(sys.argv) == 2:
        try:
            increment = float(sys.argv[1])
        except ValueError:
            debug = sys.argv[1]
    elif len(sys.argv) == 3:
        debug, increment = sys.argv[1], float(sys.argv[2])

    main(increment, debug)
