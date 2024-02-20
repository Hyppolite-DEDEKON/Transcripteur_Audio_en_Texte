import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.editor import VideoFileClip

class ConvertisseurMP4MP3:
    def __init__(self, root):
        self.root = root
        self.root.title("Convertisseur MP4 vers MP3")

        self.root.geometry("400x200")

        # Créer les étiquettes et les boutons
        self.label_entree = tk.Label(root, text="Sélectionnez le fichier MP4 :")
        self.label_entree.pack()

        self.bouton_parcourir = tk.Button(root, text="Parcourir", command=self.selectionner_fichier)
        self.bouton_parcourir.pack()

        self.label_sortie = tk.Label(root, text="Sélectionnez le dossier de sortie :")
        self.label_sortie.pack()

        self.bouton_parcourir_sortie = tk.Button(root, text="Parcourir", command=self.selectionner_dossier_sortie)
        self.bouton_parcourir_sortie.pack()

        self.bouton_convertir = tk.Button(root, text="Convertir", command=self.convertir)
        self.bouton_convertir.pack()

        self.chemin_entree = tk.StringVar()
        self.chemin_sortie = tk.StringVar()

    def selectionner_fichier(self):
        fichier = filedialog.askopenfilename(filetypes=[("Fichiers MP4", "*.mp4")])
        self.chemin_entree.set(fichier)

    def selectionner_dossier_sortie(self):
        dossier = filedialog.askdirectory()
        self.chemin_sortie.set(dossier)

    def convertir(self):
        chemin_entree = self.chemin_entree.get()
        chemin_sortie = self.chemin_sortie.get()

        if chemin_entree and chemin_sortie:
            try:
                clip = VideoFileClip(chemin_entree)
                clip.audio.write_audiofile(f"{chemin_sortie}/audio.mp3", codec='mp3')
                clip.close()
                tk.messagebox.showinfo("Conversion réussie", "La conversion a été effectuée avec succès.")
            except Exception as e:
                tk.messagebox.showerror("Erreur", f"Erreur lors de la conversion : {str(e)}")
        else:
            tk.messagebox.showwarning("Champs vides", "Veuillez sélectionner le fichier d'entrée et le dossier de sortie.")
