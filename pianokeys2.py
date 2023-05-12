import pyaudio, struct
import numpy as np
from scipy import signal
from math import sin, cos, pi
import tkinter as Tk

BLOCKLEN   = 64        # Number of frames per block
WIDTH       = 2         # Bytes per sample
CHANNELS    = 1         # Mono
RATE        = 16000      # Frames per second

MAXVALUE = 2**15-1  # Maximum allowed output signal value (because WIDTH = 2)

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
KEYPRESS = False

# Parameters
Ta = 2      # Decay time (seconds)
f0 = 440

# Calculate the filter coefficients for the new frequency
om1 = 2.0 * pi * float(f0) / RATE
r = 0.01 ** (1.0 / (Ta * RATE))

a = [1, -2 * r * cos(om1), r ** 2]
b = [r * sin(om1)]
ORDER = 2   # filter order
states = np.zeros(ORDER)
x = np.zeros(BLOCKLEN)

# Define the frequencies for each key
frequencies = {'113': 261.63, '119': 293.66, '101': 329.63, '114': 349.23, '116': 392, '121': 440, '117': 493.88,
               '107': 261.63, '108': 293.66, '59': 329.63, '39': 349.23,  # 中音
               '49': 523.25, '50': 587.33, '51': 659.26, '52': 698.46, '53': 783.99, '54': 880, '55': 987.77,
               '105': 523.25, '111': 587.33, '112': 659.26, '91': 698.46, '93': 783.99,  # 高音
               '56': 1046.5, '57': 1174.66, '48': 1318.51, '45': 1396.91, '61': 1567.98,  # 倍高音
               '97': 130.81, '115': 146.83, '100': 164.81, '102': 174.61, '103': 196, '104': 220, '106': 246.94,
               '44': 130.81, '46': 146.83, '47': 164.81,  # 低音
               '122': 65.41, '120': 73.42, '99': 82.41, '118': 87.31, '98': 97.999, '110': 110, '109': 123.47  # 倍低音
               }


def my_function(event):
    global CONTINUE
    global KEYPRESS
    global f0
    print('You pressed ' + event.char)

    if event.char:
        if ord(event.char) == 27:
            CONTINUE = False

        elif event.type == '2':  # Key press event
            if not KEYPRESS:
                KEYPRESS = True
                x[0] = 10000.0

            # Update Frequency
            if ord(event.char) in range(65,91):
                f0 = frequencies[str(ord(event.char)+32)]
            else:
                f0 = frequencies[str(ord(event.char))]
            print(f0)

        elif event.type == '3':  # Key release event
            if KEYPRESS:
                KEYPRESS = False
                x[0] = 0.0
    else:
        return


root = Tk.Tk()
root.bind("<KeyPress>", my_function)
root.bind("<KeyRelease>", my_function)

print('Press keys for sound.')
print('Press "Esc" to quit')

while CONTINUE:
    root.update()
    # Pole radius and angle
    r = 0.01 ** (1.0 / (Ta * RATE))  # 0.01 for 1 percent amplitude
    om1 = 2.0 * pi * float(f0) / RATE

    # Filter coefficients (second-order IIR)
    a = [1, -2 * r * cos(om1), r ** 2]
    b = [r * sin(om1)]

    # if KEYPRESS and CONTINUE:
    #     # Generate a new input signal for the filter
    #     # x[0] = 10000.0
    #
    # else:
    #     y = np.zeros_like(x)
    [y, states] = signal.lfilter(b, a, x, zi=states)

    x[0] = 0.0
    # KEYPRESS = False

    y = np.clip(y.astype(int), -MAXVALUE, MAXVALUE)  # Clipping

    binary_data = struct.pack('h' * BLOCKLEN, *y)  # Convert to binary binary data
    stream.write(binary_data, BLOCKLEN)  # Write binary binary data to audio output

print('* Done.')

# Close audio stream
stream.stop_stream()
stream.close()
p.terminate()