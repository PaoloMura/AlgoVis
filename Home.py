# Home screen for AlgoVis

import tkinter as tk
from tkinter import ttk
import AlgoVis

# set up the window
window = tk.Tk()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int(screen_width / 2 - 250)
y = int(screen_height / 2 - 250)
window.geometry(f"400x300+{x}+{y}")


WIN_WIDTH = 50

# runs AlgoVis with the chosen algorithm
def handle_click():
    selected = cmb_algos.current()
    if selected != -1:
        again = True
        while again:
            window.withdraw()
            again = AlgoVis.run(selected)
            window.update()
            window.deiconify()


# create the UI elements
lbl_title = tk.Label(
    text="AlgoVis",
    foreground="black",
    background="grey",
    width=WIN_WIDTH
)

frm_centre = tk.Frame()

lbl_prompt = tk.Label(master=frm_centre, text="Select an algorithm:")

algos = ["Linear Search", "Binary Search", "Bubble Sort", 
        "Insertion Sort", "Merge Sort"]

cmb_algos = tk.ttk.Combobox(
    master=frm_centre,
    justify="center",
    state="readonly",
    values=algos
)

btn_start = tk.Button(
    text="Start",
    command=handle_click
)


# display the UI elements
lbl_title.pack()
lbl_prompt.grid(row=0,column=1,pady=100)
cmb_algos.grid(row=0,column=2,pady=100)
frm_centre.pack()
btn_start.pack()

window.mainloop()
