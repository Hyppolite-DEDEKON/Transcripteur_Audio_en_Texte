# interface_graphique/interface.py
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
from tkinter import scrolledtext
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
import time
import speech_recognition as sr
from convertisseur.convertisseur import ConvertisseurMP4MP3

class AudioTranscriptionApp:
    def __init__(self, master):
        self.master = master
        master.title("Transcripteur d'audio en texte")

        # Agrandir la fenêtre
        master.geometry("800x600")

        self.text_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=60, height=15)  
        self.text_area.pack(pady=10)

        self.browse_button = tk.Button(master, text="Importer un fichier", command=self.load_audio_file)
        self.browse_button.pack(pady=10)

        self.transcribe_button = tk.Button(master, text="Transcrire", command=self.transcribe_audio)
        self.transcribe_button.pack(pady=10)

        self.progress_bar = ttk.Progressbar(master, orient="horizontal", length=200, mode="determinate")
        self.progress_bar.pack(pady=10)

        self.record_button_image = ImageTk.PhotoImage(Image.open("micro.png").resize((32, 32)))
        self.record_button = tk.Button(master, image=self.record_button_image, command=self.dummy_function)
        self.record_button.pack(side=tk.TOP, pady=10)

        self.conversion_button = tk.Button(master, text="Conversion MP4 vers MP3", command=self.lancer_convertisseur)
        self.conversion_button.pack(pady=10)

    def dummy_function(self):
        # Cette fonction ne fait rien
        pass

    def load_audio_file(self):
        try:
            file_path = filedialog.askopenfilename(title="Sélectionnez un fichier audio", filetypes=[("Fichiers audio", "*.wav *.mp3")])
        except Exception as e:
            print("Error:", str(e))
            file_path = None

        if file_path and os.path.exists(file_path):
            print("File exists.")
            self.audio_file_path = file_path
        else:
            print("No file selected or access is denied.")
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, "Aucun fichier sélectionné ou accès refusé.")

    def transcribe_audio(self):
        if hasattr(self, 'audio_file_path'):
            sound = AudioSegment.from_file(self.audio_file_path)
            chunks = split_on_silence(sound, min_silence_len=500, silence_thresh=sound.dBFS-14, keep_silence=500)
            whole_text = ""

            # Ajout de la création du répertoire 'audio-chunks'
            if not os.path.exists("audio-chunks"):
                os.mkdir("audio-chunks")

            total_chunks = len(chunks)
            for i, audio_chunk in enumerate(chunks, start=1):
                chunk_filename = os.path.join("audio-chunks", f"chunk{i}.wav")
                audio_chunk.export(chunk_filename, format="wav")
                try:
                    text = self.transcribe_audio_chunk(chunk_filename)
                except sr.UnknownValueError as e:
                    print("Error:", str(e))
                    text = ""
                else:
                    text = f"{text.capitalize()}. "
                    whole_text += text

                # Mettez à jour la barre de progression
                progress_value = (i / total_chunks) * 100
                self.progress_bar["value"] = progress_value
                self.master.update_idletasks()

                # Ajoutez une petite pause pour permettre la mise à jour de l'interface graphique
                time.sleep(0.1)

            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, whole_text)

            # Notification de fin de transcription
            messagebox.showinfo("Transcription terminée", "La transcription audio est terminée.")
        else:
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, "Veuillez d'abord sélectionner un fichier audio.")

    def lancer_convertisseur(self):
        # Créer la fenêtre du convertisseur MP4 vers MP3
        convertisseur_root = tk.Toplevel(self.master)
        convertisseur = ConvertisseurMP4MP3(convertisseur_root)

        # Lancer la boucle principale de l'interface graphique du convertisseur
        convertisseur_root.mainloop()

    def transcribe_audio_chunk(self, path, language="fr-FR"):
        r = sr.Recognizer()
        with sr.AudioFile(path) as source:
            audio_listened = r.record(source)
            try:
                text = r.recognize_google(audio_listened, language=language)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
                text = ""
        return text

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioTranscriptionApp(root)
    root.mainloop()
