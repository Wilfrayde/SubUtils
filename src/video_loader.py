from moviepy.editor import VideoFileClip

def lire_video(chemin_fichier):
    # Charger la vidéo
    clip = VideoFileClip(chemin_fichier)
    
    # Lire la vidéo
    clip.preview()

    # Fermer le clip après lecture
    clip.close()

# Exemple d'utilisation
chemin_video = "/home/dev/Bureau/video.mp4"
lire_video(chemin_video)