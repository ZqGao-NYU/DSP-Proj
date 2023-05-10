import tkinter as Tk
import pyaudio
from keyui import DEF_WIDTH, DEF_HEIGHT,create_ui
from pianokeys import PA_FORMAT, frequencies, update, np, Ta, f0, CHANNELS, RATE, BLOCKLEN, ORDER

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
        self.buttons, self.btnLabels = create_ui(self.root, None, self.__on_mouse_release, self.__on_mouse_click, self.__on_key_press, self.__on_key_release)

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
        self.states = np.zeros(ORDER)
        self.x = np.zeros(BLOCKLEN)
        self.y = np.zeros(BLOCKLEN)
        while self.CONTINUE:
            self.root.update()
            self.states = update(self.stream, self.f0,  self.KEYPRESS, Ta, self.x, self.states, self.y)
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
        if event.char.isalnum():
            # Update Frequency
            if ord(event.char) in range(65, 91):
                self.f0 = frequencies[str(ord(event.char) + 32)]
            else:
                self.f0 = frequencies[str(ord(event.char))]
            print(self.f0)
            self.KEYPRESS["KEYPRESS"] = True

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

        self.KEYPRESS["KEYPRESS"] = False
    def __on_mouse_click(self, event):
        keysm = event.widget.button_name
        if keysm == 'Escape':
            self.CONTINUE = False
            return
        if keysm in self.buttons:
            btn = self.buttons[keysm]
            btn.config(bg="gray")
            for label in self.btnLabels[btn]:
                if label:
                    label.config(bg="gray")

            if keysm.isalnum():
                # Update Frequency
                if ord(keysm) in range(65, 91):
                    self.f0 = frequencies[str(ord(keysm) + 32)]
                else:
                    self.f0 = frequencies[str(ord(keysm))]
                print(self.f0)
            self.KEYPRESS["KEYPRESS"] = True
    def __on_mouse_release(self, event):
        keysm = event.widget.button_name
        print(keysm)
        if keysm in self.buttons:
            btn = self.buttons[keysm]
            btn.config(bg="#333")
            for label in self.btnLabels[btn]:
                if label:
                    label.config(bg="#333")

            self.KEYPRESS["KEYPRESS"] = False

if __name__ == "__main__":
    PianoSimulator()
