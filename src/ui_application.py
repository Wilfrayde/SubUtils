import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from align_subtitles_with_video import extraire_audio, transcrire_audio, segmenter_audio, generer_srt, ajouter_sous_titres
import os

class SubtitleApp:
    def __init__(self, root):
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
        # Video selection
        tk.Label(self.root, text="Select Video:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.video_path, width=50).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(self.root, text="Browse", command=self.browse_video).grid(row=0, column=2, padx=10, pady=10)

        # Output selection
        tk.Label(self.root, text="Output Path:").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.output_path, width=50).grid(row=1, column=1, padx=10, pady=10)
        tk.Button(self.root, text="Browse", command=self.browse_output).grid(row=1, column=2, padx=10, pady=10)

        # Subtitle customization
        tk.Label(self.root, text="Font Size:").grid(row=2, column=0, padx=10, pady=10)
        tk.OptionMenu(self.root, self.fontsize, 20, 24, 28, 32, 36).grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Text Color:").grid(row=3, column=0, padx=10, pady=10)
        tk.OptionMenu(self.root, self.color, 'white', 'yellow', 'red', 'green', 'blue').grid(row=3, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Background Color:").grid(row=4, column=0, padx=10, pady=10)
        tk.OptionMenu(self.root, self.bg_color, 'none', 'black', 'gray', 'white').grid(row=4, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Position:").grid(row=5, column=0, padx=10, pady=10)
        tk.OptionMenu(self.root, self.position, 'bottom', 'top').grid(row=5, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Font:").grid(row=6, column=0, padx=10, pady=10)
        tk.OptionMenu(self.root, self.font, 'Arial', 'Courier', 'Helvetica', 'Times').grid(row=6, column=1, padx=10, pady=10)

        # Progress bar
        self.progress = ttk.Progressbar(self.root, orient='horizontal', length=300, mode='determinate')
        self.progress.grid(row=7, column=0, columnspan=3, pady=20)

        # Process button
        tk.Button(self.root, text="Generate Subtitled Video", command=self.process_video).grid(row=8, column=0, columnspan=3, pady=20)

    def browse_video(self):
        filename = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.mkv *.mov")])
        if filename:
            self.video_path.set(filename)

    def browse_output(self):
        filename = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
        if filename:
            self.output_path.set(filename)

    def process_video(self):
        video_path = self.video_path.get()
        output_path = self.output_path.get()
        fontsize = self.fontsize.get()
        color = self.color.get()
        bg_color = self.bg_color.get()
        position = self.position.get()
        font = self.font.get()

        if not video_path or not output_path:
            messagebox.showerror("Error", "Please select both input video and output path.")
            return

        try:
            # Reset progress bar
            self.progress['value'] = 0
            self.root.update_idletasks()

            # Process video
            chemin_audio = "audio_extrait.wav"
            chemin_srt = "sous_titres.srt"

            extraire_audio(video_path, chemin_audio)
            self.progress['value'] = 20
            self.root.update_idletasks()

            texte_transcrit = transcrire_audio(chemin_audio)
            self.progress['value'] = 40
            self.root.update_idletasks()

            segments = segmenter_audio(chemin_audio)
            self.progress['value'] = 60
            self.root.update_idletasks()

            generer_srt(texte_transcrit, chemin_srt, segments)
            self.progress['value'] = 80
            self.root.update_idletasks()

            ajouter_sous_titres(video_path, chemin_srt, output_path, fontsize, color, bg_color if bg_color != 'none' else None, position, font)
            self.progress['value'] = 100
            self.root.update_idletasks()

            # Supprimer les fichiers temporaires
            os.remove(chemin_audio)
            os.remove(chemin_srt)

            messagebox.showinfo("Success", "Subtitled video created successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = SubtitleApp(root)
    root.mainloop()