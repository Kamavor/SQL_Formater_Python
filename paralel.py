from tkinter import *
import tkinter.ttk as ttk
import time, threading

root = Tk()

pb = ttk.Progressbar(root, mode="determinate")
pb.pack()

def progress():
    for i in range(20):
        pb['value'] += i
        time.sleep(.1)

threading.Thread(target=progress).start()
root.mainloop()