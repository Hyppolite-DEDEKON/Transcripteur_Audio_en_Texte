import tkinter as tk
from tkinter import filedialog
import speech_recognition as sr

class TranscriptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Transcription Vocale en Texte")

        self.label = tk.Label(root, text="Sélectionnez un fichier audio ou enregistrez depuis le microphone:")
        self.label.pack(pady=10)

        self.transcription_text = tk.Text(root, height=10, width=50)
        self.transcription_text.pack(pady=10)

        self.browse_button = tk.Button(root, text="Parcourir", command=self.browse_file)
        self.browse_button.pack(pady=5)

        self.record_button = tk.Button(root, text="Enregistrer depuis le microphone", command=self.toggle_recording)
        self.record_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Arrêter l'enregistrement", command=self.stop_recording)
        self.stop_button.pack(pady=5)
        self.stop_button["state"] = "disabled"  # Désactiver le bouton d'arrêt initialement

        # Gestion de l'événement de fermeture de la fenêtre
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.recording = False  # Indicateur d'enregistrement en cours
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def browse_file(self):
        file_path = filedialog.askopenfilename(title="Sélectionnez un fichier audio", filetypes=[("Fichiers audio", "*.wav *.mp3")])
        if file_path:
            self.transcribe_audio(file_path)

    def toggle_recording(self):
        if not self.recording:
            self.recording = True
            self.stop_button["state"] = "normal"
            self.record_button["state"] = "disabled"

            with self.microphone as source:
                print("Enregistrement audio. Parlez maintenant...")
                self.audio = self.recognizer.listen(source, timeout=None)  
                print("Enregistrement terminé.")
                if self.recording:
                    self.transcribe_audio(None)
        else:
            self.stop_recording()

    def stop_recording(self):
        self.recording = False
        self.stop_button["state"] = "disabled"
        self.record_button["state"] = "normal"

    def transcribe_audio(self, audio_file):
        if audio_file:
            audio = sr.AudioFile(audio_file)
            with audio as source:
                audio_data = self.recognizer.record(source)
        else:
            audio_data = self.audio

        try:
            text = self.recognizer.recognize_google(audio_data)
            self.transcription_text.delete(1.0, tk.END)
            self.transcription_text.insert(tk.END, text)
        except sr.UnknownValueError:
            self.transcription_text.delete(1.0, tk.END)
            self.transcription_text.insert(tk.END, "Google Speech Recognition n'a pas pu comprendre l'audio.")
        except sr.RequestError as e:
            self.transcription_text.delete(1.0, tk.END)
            self.transcription_text.insert(tk.END, f"Erreur lors de la demande à l'API Google Speech Recognition : {e}")

    def on_closing(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TranscriptionApp(root)
    root.mainloop()





