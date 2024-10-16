import sys
import os
import tkinter as tk

# Ajouter le chemin du répertoire src au sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from ui_application import SubtitleApp

if __name__ == "__main__":
    root = tk.Tk()
    app = SubtitleApp(root)
    root.mainloop()