## Digital Signal Processing LAB I Project Report 

**Ziqi Gao (zg2346@nyu.edu**) **Loki Zhou (lz2944@nyu.edu)**

### Basic Idea 

The idea of this simulator came from the demo 18, where we are required to design a program in which you can make octave of notes through pressing the keys on the keyboard. 

This project extends the demo 18 by adding a GUI part and supporting more frequencies. Also the operation after the users presses the keys are also adjusted to simulate a piano. Those two parts will be introduced later.

### File Structure

This simulator consists of the following three files:

> main.py     The main class of the project. Integrate the UI and Simulator together.
>
> keyui.py     The implementation of the GUI
>
> pianokeys.py      The implementation of the sound simulation part

You can use `python main.py` to interpret and execute it. 

Please install the following libraries in advance:

> pyaudio
>
> tkinter
>
> numpy

Or you can go to this link to download the executable file (due to the limitations of the pyinstall library, the file is really large for 350MB) :

> https://drive.google.com/file/d/1afdR8111BwcH09V4CClt3TrGMLhOuuLQ/view?usp=share_link

### GUI Part

The GUI of the project is very similar to the layout of the common keyboard on the PC. And all of the keys are remapped to the numeric musical notation.

![image-20230512224906032](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20230512224906032.png)

Here is the details of the implementation:

- Firstly, create a key-numeric note-frequency mapping.
- Design the UI, and marks the keys with special width like `Tab`, `Space`, `Shift` etc. 
- For the dots above or below the number, they are achieved by labels which are attached to the button and their location are sets specially to make the UI looks good in general. 
- Use for loop to iterate through all the mappings and set up the text, name for the buttons.
- Finally, the `keypress`, `keyrelease`, `mouseclick`, `mouserelease` events are set in the `main.py` since it requires some nonlocal variables to integrate the simulator with GUI together.
-  `keypress`, `keyrelease`, `mouseclick`, `mouserelease` functions are vital for the simulation of the sound for they will set the variables for the simulation part to do the following calculation. This works with the key-note-frequency mapping.

### Sound Simulation Part

In this module we refer to what we learned in class and simulate the sound of piano keys through keyboard keys.

Here is how the code works:

- First import the necessary modules: *pyaudio*, *struct*, *numpy*, *scipy.signal*, *math* and *tkinter*.

-  Define several parameters.

  - BLOCKLEN: number of frames per block.

  - WIDTH: number of bytes per sample.

  - CHANNELS: number of audio channels.

  - RATE: number of frames per second

- The PyAudio stream is turned on for audio output.

- We use a filter to filter the output signal. The coefficients of the filter (*a* and *b*) are calculated based on the desired frequency (*f0*) and the decay time (*Ta*).

- Use a dictionary to store the frequency of the scale corresponding to each key, the key is the ASCII value of the symbol corresponding to the key, and the value is the corresponding frequency.

- *my_function* is a callback function that handles key press and release events. It updates the global variables *CONTINUE*, *KEYPRES*, *f0* and *x[0]* based on the keypress event. If *KEYPRES* is recognized as *True*, it means the key is pressed, *x[0]* is set to *10000* and *f0* is updated to the frequency corresponding to the key, if *KEYPRES* is recognized as *Flase*, it means the key is released, *x[0]* is set to *0* and the sound stops playing.

- *update* is designed to update the filter coefficients and the input signal (*x*), which is updated according to key events.

- The program will continue to loop until the *CONTINUE* variable is set to *False* or the user presses the "Esc" key.

- At the end of the loop, the audio stream is closed and the PyAudio instance is terminated.

- The PyAudio stream is turned on for audio output.

- We use a filter to filter the output signal. The coefficients of the filter (*a* and *b*) are calculated based on the desired frequency (*f0*) and the decay time (*Ta*).

- Use a dictionary to store the frequency of the scale corresponding to each key, the key is the ASCII value of the symbol corresponding to the key, and the value is the corresponding frequency.

- *my_function* is a callback function that handles key press and release events. It updates the global variables *CONTINUE*, *KEYPRES*, *f0* and *x[0]* based on the keypress event. If *KEYPRES* is recognized as *True*, it means the key is pressed, *x[0]* is set to *10000* and *f0* is updated to the frequency corresponding to the key, if *KEYPRES* is recognized as *Flase*, it means the key is released, *x[0]* is set to *0* and the sound stops playing.

- *update* is designed to update the filter coefficients and the input signal (*x*), which is updated according to key events.

- The program will continue to loop until the *CONTINUE* variable is set to *False* or the user presses the "Esc" key.

- At the end of the loop, the audio stream is closed and the PyAudio instance is terminated.

- Also, the implementation is adjusted to simulate the situation where the user press and hold one key for some time. Instead of keeping regenerate the original wave, it will not generate new wave until the user release the key, and the sound of it will go lighter and lighter until silence. 
- For the chords part, it is necessary to use some data structures like dictionary to keep the states of each notes pressed. And to maintain the purity of the sound, some waves with very small states values are removed in advance. 



### Further Development

To improve the performance of it, there are following directions:

- Find better algorithm to simulate the sound of piano instead of sinusoid
- Implement the functions of pedals (soft pedal and sustain pedal).





Group Members:

****Ziqi Gao ([zg2346@nyu.edu](mailto:zg2346@nyu.edu)****) ****Loki Zhou ([lz2944@nyu.edu](mailto:lz2944@nyu.edu))****
This simulator consists of the following three files:



> main.py The main class of the project. Integrate the UI and Simulator together.
>
> keyui.py The implementation of the GUI
>
> pianokeys.py The implementation of the sound simulation part

You can use ``python main.py`` to interpret and execute it. 

Please install the following libraries in advance:

> pyaudio
>
> tkinter
>
> numpy



Or you can go to this link to download the executable file (due to the limitations of the pyinstall library, the file is really large for 350MB) :

> https://drive.google.com/file/d/1afdR8111BwcH09V4CClt3TrGMLhOuuLQ/view?usp=share_link
