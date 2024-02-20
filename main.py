import tkinter as tk
from interface_graphique.interface import AudioTranscriptionApp

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioTranscriptionApp(root)
    root.mainloop()
