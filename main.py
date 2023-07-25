import tkinter as Tk

import pyaudio
from keyui import DEF_WIDTH, DEF_HEIGHT, create_ui
from pianokeys import PA_FORMAT, frequencies, update, np, Ta,  CHANNELS, RATE, BLOCKLEN, ORDER, mapping


class PianoSimulator:
    def __init__(self):
        self.RATE = 8000
        self.CHANNELS = 1
        self.__init_ui()
        self.__init_audio()

    def __init_ui(self):
        self.CONTINUE = True
        self.KEYPRESS = {"KEYPRESS": False}
        self.root = Tk.Tk()
        self.root.title("Piano Simulator")
        self.root.geometry(f"{DEF_WIDTH - 80}x{DEF_HEIGHT - 40}")
        self.root.configure(bg="black")
        self.buttons, self.btnLabels = create_ui(self.root, None, self.__on_mouse_release, self.__on_mouse_click,
                                                 self.__on_key_press, self.__on_key_release)

    def __init_audio(self):
        # Open the audio output stream
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=PA_FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=False,
            output=True,
            frames_per_buffer=128)
        self.f0 = 440
        self.notes = {}
        self.states = np.zeros(ORDER)
        while self.CONTINUE:
            self.root.update()
            update(self.stream, Ta,  self.states, self.notes)
        print('* Done.')
        self.root.destroy()
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def __on_key_press(self, event):
        print('You pressed ' + event.keysym)
        if event.keysym == 'Escape':
            self.CONTINUE = False
            return
        if event.char:
            # Update Frequency
            if ord(event.char) in range(65, 91):
                self.f0 = frequencies[str(ord(event.char) + 32)]
            else:
                self.f0 = frequencies[str(ord(event.char))]
            if not self.notes.get(event.keysym):
                x = np.zeros(BLOCKLEN)
                x[0] = 10000
                self.notes[event.keysym] = [self.f0, x, True, np.zeros(ORDER)]
            elif not self.notes[event.keysym][2]:
                self.notes[event.keysym][1][0] = 10000
                self.notes[event.keysym][2] = True
            else:
                self.notes[event.keysym][1][0] = 0
        if event.keysym in self.buttons:

            btn = self.buttons[event.keysym]

            btn.config(bg="gray")

            for label in self.btnLabels[btn]:

                if label:
                    label.config(bg="gray")

    def __on_key_release(self, event):
        if event.keysym in self.buttons:
            btn = self.buttons[event.keysym]
            btn.config(bg="#333")
            for label in self.btnLabels[btn]:
                if label:
                    label.config(bg="#333")
        if event.keysym in self.notes:
            self.notes[event.keysym][2] = False
            self.notes[event.keysym][1] = np.zeros(BLOCKLEN)

    def __on_mouse_click(self, event):
        keysym = event.widget.button_name
        print('You clicked ' + keysym)
        if keysym == 'Escape':
            self.CONTINUE = False
            return
        if keysym in self.buttons:
            btn = self.buttons[keysym]
            btn.config(bg="gray")
            for label in self.btnLabels[btn]:
                if label:
                    label.config(bg="gray")

            try:
                if keysym.isalnum():
                    # Update Frequency
                    if ord(keysym) in range(65, 91):
                        self.f0 = frequencies[str(ord(keysym) + 32)]
                    else:
                        self.f0 = frequencies[str(ord(keysym))]
            except TypeError:
                if keysym in mapping:
                    key = mapping[keysym]
                    self.f0 = frequencies[str(ord(key))]
            if keysym in mapping or keysym.isalnum():
                if not self.notes.get(keysym):
                    x = np.zeros(BLOCKLEN)
                    x[0] = 10000
                    self.notes[keysym] = [self.f0, x, True, np.zeros(ORDER)]
                elif not self.notes[keysym][2]:
                    self.notes[keysym][1][0] = 10000
                    self.notes[keysym][2] = True
                else:
                    self.notes[keysym][1][0] = 0

    def __on_mouse_release(self, event):
        keysym = event.widget.button_name
        if keysym in self.buttons:
            btn = self.buttons[keysym]
            btn.config(bg="#333")
            for label in self.btnLabels[btn]:
                if label:
                    label.config(bg="#333")
        if keysym in self.notes:
            self.notes[keysym][2] = False
            self.notes[keysym][1] = np.zeros(BLOCKLEN)


if __name__ == "__main__":
    PianoSimulator()
