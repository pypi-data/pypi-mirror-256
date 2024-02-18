import os
import math
import shutil
import string
import os.path as path

import mido

from .plmidi_cpp import sound as _sound, plmidi_KeyBordInterrupt

OUTPUT_MIDI_NAME: str = "._Plm_temp_.mid"

def sound(midifile: str):
    if not isinstance(midifile, str) and not path.exists(midifile):
        raise TypeError
    
    ascii_chars = tuple(string.ascii_letters + string.digits + string.punctuation + " ")
    for char in midifile:
        if char not in ascii_chars:
            shutil.copy(midifile, OUTPUT_MIDI_NAME)
            midifile = OUTPUT_MIDI_NAME
            break

    midi_duration = 0
    for msg in mido.MidiFile(midifile, clip=True):
        midi_duration += msg.time

    try:
        _sound(midifile, math.ceil(midi_duration))
    except plmidi_KeyBordInterrupt:
        pass

    if path.exists(OUTPUT_MIDI_NAME):
        os.remove(OUTPUT_MIDI_NAME)