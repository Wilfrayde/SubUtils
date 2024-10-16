from moviepy.editor import VideoFileClip
import speech_recognition as sr
import pysrt

def extraire_audio(chemin_video, chemin_audio):
    # Charger la vidéo
    clip = VideoFileClip(chemin_video)
       
    # Extraire l'audio
    clip.audio.write_audiofile(chemin_audio)

def transcrire_audio(chemin_audio):
    # Initialiser le recognizer
    recognizer = sr.Recognizer()
       
    # Charger l'audio
    with sr.AudioFile(chemin_audio) as source:
        audio = recognizer.record(source)
       
    # Transcrire l'audio en texte
    texte = recognizer.recognize_google(audio, language='fr-FR')
    return texte

def generer_srt(texte_transcrit, chemin_srt):
    # Créer un fichier SRT à partir du texte transcrit
    sous_titres = pysrt.SubRipFile()
       
    # Exemple simple : un seul sous-titre pour tout le texte
    sous_titre = pysrt.SubRipItem(index=1, start=pysrt.SubRipTime(0, 0, 0), end=pysrt.SubRipTime(0, 1, 0), text=texte_transcrit)
    sous_titres.append(sous_titre)
       
    # Enregistrer le fichier SRT
    sous_titres.save(chemin_srt, encoding='utf-8')

# Exemple d'utilisation
if __name__ == "__main__":
    chemin_video = "/home/dev/Bureau/video.mp4"
    chemin_audio = "/home/dev/Bureau/SubUtils/audio/audio.wav"
    chemin_srt = "/home/dev/Bureau/SubUtils/srt/fichier.srt"
       
    extraire_audio(chemin_video, chemin_audio)
    texte_transcrit = transcrire_audio(chemin_audio)
    generer_srt(texte_transcrit, chemin_srt)