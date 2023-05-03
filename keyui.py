from tkinter import Tk, Frame, Button, Label
from tkinter.font import Font as font

DEF_WIDTH = 1400
DEF_HEIGHT = 300

root = Tk()
root.title("Piano Simulator")
root.geometry(f"{DEF_WIDTH - 80}x{DEF_HEIGHT - 40}")
root.configure(bg="black")
# root.attributes("-topmost", True)
root.resizable(False, False)

ACCENT_COL = "red"

row1 = ["ESC", ".1", ".2", ".3", ".4", ".5", ".6", ".7", "..1", "..2", "..3", "..4", "..5",
        "Backspace"]  # Higher + Highest
row2 = ["Tab", "1", "2", "3", "4", "5", "6", "7", ".1", ".2", ".3", ".4", ".5", "\\|"]  # Standard + Higher
row3 = ["Caps", "1.", "2.", "3.", "4.", "5.", "6.", "7.", "1", "2", "3", "4", "Enter"]  # Lower + Standard
row4 = ["Shift", "1..", "2..", "3..", "4..", "5..", "6..", "7..", "1.", "2.", "3.",
        "Shift R"]  # Lowest + Lower
row5 = ["Ctrl", "Win", "Alt", "", "Alt", "Win","Menu", "Ctrl"]

rows = [row1, row2, row3, row4, row5]

width15 = ["Backspace", "Tab"]
width175 = ["Caps","Enter"]
width225 = ["Shift", "Shift R"]
width55 = [""]

highest = set(row1[8:13])
higher = set(row1[1:8] + row2[8:13])
standard = set(row2[1:8] + row3[8:12])
lower = set(row3[1:8] + row4[8:11])
lowest = set(row4[1:8])


def on_enter(e):
    pass

def on_leave(e):
    pass

def handleClick(e):
    pass


btnLabels = {}
allButtons = []
Y = 2.5

for r in rows:
    X = 5
    for i in r:
        btnWidth = 0.06428 * DEF_WIDTH
        btnHeight = 0.16666 * DEF_HEIGHT
        padx = round(btnWidth / 9)
        pady = round(btnHeight / 9)

        frame = Frame(root, highlightbackground="black", highlightthickness=4)  # Create a container for keys
        if i in highest or i in lowest:
            anchor = "s"
            label1 = Label(root, text=".", fg="#fff", bg="#333", font=font(size=10),  padx=0, pady=0, bd=0)
            label2 = Label(root, text=".", fg="#fff", bg="#333", font=font(size=10), padx=0, pady=0, bd=0)
            if i in lowest:
                anchor = "n"
                label2.place(x=X + 0.5*padx + 41, y=Y + 2 * pady + 23)
                label1.place(x=X + 0.5*padx + 41, y=Y + 2 * pady + 13)
                i = i[0]
            else:
                label1.place(x=X + 0.5 * padx + 41, y=Y + pady - 2)
                label2.place(x=X + 0.5 * padx + 41, y=Y + pady + 10)
                i = i[-1]

        elif i in higher or i in lower:
            anchor = "s"
            label1 = Label(root, text=".", fg="#fff", bg="#333", font=font(size=11))
            label2 = None
            if i in lower:
                anchor = "n"
                label1.place(x=X + 0.5*padx + 39, y=Y + 2 * pady + 13)
                i = i[0]
            else:
                label1.place(x=X + 0.5 * padx + 39, y=Y + pady - 2)
                i = i[-1]
        else:
            anchor = "center"
            label1 = None
            label2 = None
        btn = Button(frame, activebackground=ACCENT_COL, text=i, bg="#333", fg="#fff", relief="flat", padx=padx, pady=pady,
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

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        btn.bind("<Button-1>", handleClick)
        btn.bind("<ButtonRelease-1>", on_leave)

        btnLabels[btn] = (label1, label2)
        allButtons.append(btn)
    Y += btnHeight


root.mainloop()