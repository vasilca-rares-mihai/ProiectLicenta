import tkinter as tk
from tkinter import filedialog
import os

# Ascunde fereastra principală Tkinter
root = tk.Tk()
root.withdraw()

# Deschide dialogul pentru a alege fișierul video
initial_path = os.path.join("video", "pullups")
print(initial_path)
video_path = filedialog.askopenfilename(
    title="Alege un clip video",
    initialdir=initial_path,
    filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv")]
)
