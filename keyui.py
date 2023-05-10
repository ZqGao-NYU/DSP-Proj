from tkinter import Tk, Frame, Button, Label
from tkinter.font import Font as font

DEF_WIDTH = 1400
DEF_HEIGHT = 300


def create_ui(root, on_enter=None, on_leave=None, handleClick=None, on_key_press=None, on_key_release=None):
    root.resizable(False, False)

    ACCENT_COL = "gray"

    row1_list = ["ESC", ".1", ".2", ".3", ".4", ".5", ".6", ".7", "..1", "..2", "..3", "..4", "..5",
                 "Backspace"]  # Higher + Highest
    row1 = {"Escape": "ESC", "1": ".1", "2": ".2", "3": ".3", "4": ".4", "5": ".5", "6": ".6", "7": ".7", "8": "..1",
            "9": "..2", "0": "..3", "minus": "..4", "equal": "..5", "BackSpace": "Backspace"}
    row2_list = ["Tab", "1", "2", "3", "4", "5", "6", "7", ".1", ".2", ".3", ".4", ".5", "\\|"]  # Standard + Higher
    row2 = {"Tab": "Tab", "q": "1", "w": "2", "e": "3", "r": "4", "t": "5", "y": "6", "u": "7", "i": ".1", "o": ".2",
            "p": ".3", "bracketleft": ".4", "bracketright": ".5", "backslash": "\\|"}
    row3_list = ["Caps", "1.", "2.", "3.", "4.", "5.", "6.", "7.", "1", "2", "3", "4", "Enter"]  # Lower + Standard
    row3 = {"Caps_Lock": "Caps", "a": "1.", "s": "2.", "d": "3.", "f": "4.", "g": "5.", "h": "6.", "j": "7.", "k": "1",
            "l": "2", "semicolon": "3", "apostrophe": "4", "Return": "Enter"}
    row4_list = ["Shift", "1..", "2..", "3..", "4..", "5..", "6..", "7..", "1.", "2.", "3.",
                 "Shift R"]  # Lowest + Lower
    row4 = {"Shift_L": "Shift", "z": "1..", "x": "2..", "c": "3..", "v": "4..", "b": "5..", "n": "6..", "m": "7..",
            "comma": "1.", "period": "2.", "slash": "3.", "Shift_R": "Shift R"}
    row5_list = ["Ctrl", "Win", "Alt", "", "Alt", "Win", "Menu", "Ctrl"]
    row5 = {"Control_L": "Ctrl", "Super_L": "Win", "Alt_L": "Alt", "space": "", "Alt_R":"Alt", "Super_R":"Win", "Menu": "Menu", "Control_R":"Ctrl"}

    rows = [row1, row2, row3, row4, row5]

    width15 = ["Backspace", "Tab"]
    width175 = ["Caps", "Enter"]
    width225 = ["Shift", "Shift R"]
    width55 = [""]

    highest = set(row1_list[8:13])
    higher = set(row1_list[1:8] + row2_list[8:13])
    standard = set(row2_list[1:8] + row3_list[8:12])
    lower = set(row3_list[1:8] + row4_list[8:11])
    lowest = set(row4_list[1:8])

    btnLabels = {}
    allButtons = {}
    Y = 2.5

    for r in rows:
        X = 5
        for key, i in r.items():
            btnWidth = 0.06428 * DEF_WIDTH
            btnHeight = 0.16666 * DEF_HEIGHT
            padx = round(btnWidth / 9)
            pady = round(btnHeight / 9)

            frame = Frame(root, highlightbackground="black", highlightthickness=4)  # Create a container for keys
            if i in highest or i in lowest:
                anchor = "s"
                label1 = Label(root, text=".", activebackground="gray", fg="#fff", bg="#333", font=font(size=10),
                               padx=0, pady=0, bd=0)
                label2 = Label(root, text=".", fg="#fff", bg="#333", activebackground="gray", font=font(size=10),
                               padx=0, pady=0, bd=0)
                if i in lowest:
                    anchor = "n"
                    label2.place(x=X + 0.5 * padx + 41, y=Y + 2 * pady + 23)
                    label1.place(x=X + 0.5 * padx + 41, y=Y + 2 * pady + 13)
                    i = i[0]
                else:
                    label1.place(x=X + 0.5 * padx + 41, y=Y + pady - 2)
                    label2.place(x=X + 0.5 * padx + 41, y=Y + pady + 10)
                    i = i[-1]

            elif i in higher or i in lower:
                anchor = "s"
                label1 = Label(root, text=".", activebackground="gray", fg="#fff", bg="#333", font=font(size=11))
                label2 = None
                if i in lower:
                    anchor = "n"
                    label1.place(x=X + 0.5 * padx + 39, y=Y + 2 * pady + 13)
                    i = i[0]
                else:
                    label1.place(x=X + 0.5 * padx + 39, y=Y + pady - 2)
                    i = i[-1]
            else:
                anchor = "center"
                label1 = None
                label2 = None
            btn = Button(frame, activebackground=ACCENT_COL, text=i, bg="#333", fg="#fff", relief="flat", padx=padx,
                         pady=pady,
                         font=font(size=10), anchor=anchor)

            # Reset the button's width
            if i in width15:
                btnWidth = 1.5 * btnWidth
            elif i in width175:
                btnWidth = 1.75 * btnWidth
            elif i in width225:
                btnWidth = 2.25 * btnWidth
            elif i in width55:
                btnWidth = 7.5 * btnWidth

            btn.place(x=0, y=0, width=btnWidth, height=btnHeight)
            frame.place(x=X, y=Y, width=btnWidth, height=btnHeight)
            X += btnWidth

            # btn.bind("<Enter>", on_enter)
            # btn.bind("<Leave>", on_leave)
            # btn.bind("<Button-1>", handleClick)
            # btn.bind("<ButtonRelease-1>", on_leave)
            root.bind("<KeyPress>", on_key_press)
            root.bind("<KeyRelease>", on_key_release)

            btnLabels[btn] = (label1, label2)
            allButtons[key] = btn
        Y += btnHeight
    return allButtons, btnLabels
