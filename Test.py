# keyboard_demo_06.py
# Play a note using a second-order difference equation
# when the user presses a key on the keyboard.

import pyaudio, struct
import numpy as np
from scipy import signal
from math import sin, cos, pi
import tkinter as Tk

BLOCKLEN   = 64        # Number of frames per block
WIDTH       = 2         # Bytes per sample
CHANNELS    = 1         # Mono
RATE        = 8000      # Frames per second

MAXVALUE = 2**15-1  # Maximum allowed output signal value (because WIDTH = 2)

# Parameters
Ta = 2      # Decay time (seconds)
f0 = 440    # Frequency (Hz) Middle A

# Pole radius and angle
r = 0.01**(1.0/(Ta*RATE))       # 0.01 for 1 percent amplitude
om1 = 2.0 * pi * float(f0)/RATE

# Filter coefficients (second-order IIR)
a = [1, -2*r*cos(om1), r**2]
b = [r*sin(om1)]
ORDER = 2   # filter order
states = np.zeros(ORDER)
x = np.zeros(BLOCKLEN)
notes = 12 * [[b, a, states]]
cur_idx = 0
# Open the audio output stream
p = pyaudio.PyAudio()
PA_FORMAT = pyaudio.paInt16
stream = p.open(
        format      = PA_FORMAT,
        channels    = CHANNELS,
        rate        = RATE,
        input       = False,
        output      = True,
        frames_per_buffer = 128)
# specify low frames_per_buffer to reduce latency

CONTINUE = True
KEYPRESS = [False] * 12

def my_function(event):
    global CONTINUE
    global cur_idx
    if event.char == 'q':
      print('Good bye')
      CONTINUE = False
    else:
        # Update Frequency
        if not event.char: return
        KEYPRESS[cur_idx] = True
        f0 = 2 ** ((ord(event.char) - ord('a')) % 12 / 12) * 440
        print(f0)
        om1 =  2.0 * pi * float(f0)/RATE
        a = [1, -2 * r * cos(om1), r ** 2]
        b = [r * sin(om1)]
        notes[cur_idx] = [b, a, notes[cur_idx][2]]
        cur_idx += 1

root = Tk.Tk()
root.bind("<Key>", my_function)

print('Press keys for sound.')
print('Press "q" to quit')

while CONTINUE:
    root.update()

    this_y = [0] * 64
    for i in range(12):
        if KEYPRESS[i]:
            x[0] = 10000.0
        else:
            x[0] = 0
        b, a, states = notes[i]
        [y, states] = signal.lfilter(b, a, x, zi = states)
        y = np.clip(y.astype(int), -MAXVALUE, MAXVALUE)
        notes[i][2] = states
        this_y = np.add(this_y, y)
    cur_idx = 0
    x[0] = 0.0
    KEYPRESS = [False] * 12
    # stream.write(this_y.tobytes())

    binary_data = struct.pack('h' * BLOCKLEN, *this_y)     # Convert to binary binary data
    stream.write(binary_data, BLOCKLEN)               # Write binary binary data to audio output

print('* Done.')

# Close audio stream
stream.stop_stream()
stream.close()
p.terminate()
