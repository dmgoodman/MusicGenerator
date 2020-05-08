# MusicGenerator - COS 401 Final Project
## About

Using MIDI audio files of piano compositions by classical composers, such as Bach, Beethoven, Brahms, Chopin, Mozart, and Schubert, we generated new MIDI audio files using multiple orders of Markov Models. Our training data consists of some of the most famous single-instrument compositions of our chosen composers in the MIDI audio format. By observing the frequencies and positions of different notes/tempos in these pieces, we generate MIDI audio files de novo that take into account the styles and chord progressions of established, classical music. We test multiple orders of the Markov Model to determine how far back in a piece of music we must look to determine the next note as certain music chord/note progressions are often less appealing than others. These generated MIDI files (found in the folder midi_generated) can be played using an [online MIDI sequencer](https://onlinesequencer.net/import).

## Folder Contents

midi_audio: Contains training audio files collected from online sources.  
midi_discretized: Contains completely preprocessed data in discrete, non-overlapping intervals.  
midi_generated: Contains Markov-generated MIDI files along with their .json representation.  
midi_messages: Contains all messages of training audio files (used for reference only).  
midi_processed: Contains first step preprocessed data (removed overlapping intervals).  

## Authors

Daniel Goodman, Lachlan McCarty, Sriram Srinivasan