import tkinter as tk
import traceback
from tkinter import ttk, filedialog, messagebox
from align_subtitles_with_video import extraire_audio, transcrire_audio, segmenter_audio, generer_srt, ajouter_sous_titres
import os
import threading

class SubtitleApp:
    """
    Application GUI pour ajouter des sous-titres à une vidéo.
    """

    def __init__(self, root):
        """
        Initialise l'application avec les éléments de l'interface utilisateur.

        :param root: Fenêtre principale de l'application.
        """
        self.root = root
        self.root.title("Subtitle Application")

        # Variables
        self.video_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.fontsize = tk.IntVar(value=24)
        self.color = tk.StringVar(value='white')
        self.bg_color = tk.StringVar(value='none')
        self.position = tk.StringVar(value='bottom')
        self.font = tk.StringVar(value='Arial')

        # UI Elements
        self.create_widgets()

    def create_widgets(self):
        """
        Crée les widgets de l'interface utilisateur.
        """
        tk.Label(self.root, text="Select Video:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.video_path, width=50).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(self.root, text="Browse", command=self.browse_video).grid(row=0, column=2, padx=10, pady=10)

        tk.Label(self.root, text="Output Path:").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.output_path, width=50).grid(row=1, column=1, padx=10, pady=10)
        tk.Button(self.root, text="Browse", command=self.browse_output).grid(row=1, column=2, padx=10, pady=10)

        tk.Label(self.root, text="Font Size:").grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.fontsize, width=10).grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Text Color:").grid(row=3, column=0, padx=10, pady=10)
        ttk.Combobox(self.root, textvariable=self.color, values=['white', 'black', 'red', 'green', 'blue']).grid(row=3, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Background Color:").grid(row=4, column=0, padx=10, pady=10)
        ttk.Combobox(self.root, textvariable=self.bg_color, values=['none', 'black', 'white']).grid(row=4, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Position:").grid(row=5, column=0, padx=10, pady=10)
        ttk.Combobox(self.root, textvariable=self.position, values=['bottom', 'top', 'center']).grid(row=5, column=1, padx=10, pady=10)

        tk.Button(self.root, text="Start", command=self.start_processing).grid(row=6, column=1, pady=20)

        # Barre de progression
        self.progress = ttk.Progressbar(self.root, orient='horizontal', length=300, mode='indeterminate')
        self.progress.grid(row=7, column=0, columnspan=3, pady=20)

    def browse_video(self):
        """
        Ouvre une boîte de dialogue pour sélectionner un fichier vidéo.
        """
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov")])
        if file_path:
            self.video_path.set(file_path)

    def browse_output(self):
        """
        Ouvre une boîte de dialogue pour sélectionner le chemin de sortie.
        """
        file_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
        if file_path:
            self.output_path.set(file_path)

    def start_processing(self):
        """
        Démarre le traitement de la vidéo pour ajouter des sous-titres.
        """
        video_path = self.video_path.get()
        output_path = self.output_path.get()
        fontsize = self.fontsize.get()
        color = self.color.get()
        bg_color = self.bg_color.get()
        position = self.position.get()
        font = self.font.get()

        if not video_path or not output_path:
            messagebox.showerror("Erreur", "Veuillez sélectionner une vidéo et un chemin de sortie.")
            return

        self.progress.start()  # Démarre la barre de progression
        threading.Thread(target=self.process_video, args=(video_path, output_path, fontsize, color, bg_color, position, font)).start()

    def process_video(self, video_path, output_path, fontsize, color, bg_color, position, font):
        """
        Traite la vidéo pour extraire l'audio, transcrire, segmenter et ajouter des sous-titres.
        """
        try:
            chemin_audio = "temp_audio.wav"
            chemin_srt = "temp_subtitles.srt"

            extraire_audio(video_path, chemin_audio)
            texte_transcrit = transcrire_audio(chemin_audio)
            segments = segmenter_audio(chemin_audio)
            generer_srt(texte_transcrit, chemin_srt, segments)
            ajouter_sous_titres(video_path, chemin_srt, output_path, fontsize, color, bg_color if bg_color != 'none' else None, position, font)

            os.remove(chemin_audio)
            os.remove(chemin_srt)

            messagebox.showinfo("Succès", "La vidéo sous-titrée a été créée avec succès !")
        except FileNotFoundError as e:
            messagebox.showerror("Erreur", f"Fichier introuvable : {e}")
        except Exception as e:
            error_message = traceback.format_exc()
            messagebox.showerror("Erreur", f"Une erreur s'est produite :\n{error_message}")
        finally:
            self.progress.stop()  # Arrête la barre de progression