from settings import INTERFACE_FPS
import tkinter as tk
from PIL import ImageTk, Image
import time

TICK_MS = round((1/INTERFACE_FPS)*1000)

window= tk.Tk()
window.grid()
window.title("test")
window.geometry("500x500")
window.configure(background='grey')

path = "C:/Users/henry/Documents/art!/f 5-30-2024 7-02 PM - colored 128x128.png"
img = ImageTk.PhotoImage(Image.open(path))
panel = tk.Label(window, image = img)

panel.pack(side = "bottom", fill = "both", expand = "yes")

def windowProcesses():
    global window
    if round(time.time()) % 2 == 0:
        path = "C:/Users/henry/Documents/art!/f 5-30-2024 7-02 PM - colored 128x128.png"
    else: 
        path = "C:/Users/henry/Pictures/128x128/Screenshot 2023-11-23 153656.png"
    img = ImageTk.PhotoImage(Image.open(path))
    panel.configure(image = img)
    panel.image=img
    window.after(TICK_MS, windowProcesses)
        
window.after(TICK_MS, windowProcesses)
window.mainloop()