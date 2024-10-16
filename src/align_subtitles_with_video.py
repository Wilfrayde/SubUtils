from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import pysubs2
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os

def extraire_audio(chemin_video, chemin_audio):
    """
    Extrait l'audio d'une vidéo et l'enregistre dans un fichier.

    :param chemin_video: Chemin du fichier vidéo source.
    :param chemin_audio: Chemin du fichier audio de sortie.
    """
    clip = VideoFileClip(chemin_video)
    clip.audio.write_audiofile(chemin_audio)
    clip.close()

    # Vérifiez si l'audio est lisible
    try:
        audio = AudioSegment.from_wav(chemin_audio)
        print("Audio extrait avec succès.")
    except Exception as e:
        raise Exception("Erreur lors de l'extraction de l'audio : " + str(e))

def transcrire_audio(chemin_audio):
    """
    Transcrit l'audio d'un fichier en texte.

    :param chemin_audio: Chemin du fichier audio à transcrire.
    :return: Texte transcrit de l'audio.
    """
    recognizer = sr.Recognizer()
    with sr.AudioFile(chemin_audio) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        raise Exception("L'audio n'a pas pu être compris. Veuillez vérifier la qualité de l'audio.")
    except sr.RequestError:
        raise Exception("Erreur de connexion au service de reconnaissance vocale. Vérifiez votre connexion Internet.")
    
def segmenter_audio(chemin_audio):
    """
    Segmente l'audio en fonction des silences.

    :param chemin_audio: Chemin du fichier audio à segmenter.
    :return: Liste des segments audio.
    """
    audio = AudioSegment.from_wav(chemin_audio)
    return split_on_silence(audio, min_silence_len=300, silence_thresh=audio.dBFS-16)

def generer_srt(texte, chemin_srt, segments):
    """
    Génère un fichier SRT à partir du texte transcrit et des segments audio.

    :param texte: Texte transcrit de l'audio.
    :param chemin_srt: Chemin du fichier SRT de sortie.
    :param segments: Liste des segments audio.
    """
    with open(chemin_srt, 'w') as f:
        f.write("1\n00:00:00,000 --> 00:00:01,000\n" + texte + "\n")

def ajouter_sous_titres(chemin_video, chemin_sous_titres, chemin_sortie, fontsize=24, color='white', bg_color=None, position='bottom', font='Arial'):
    """
    Ajoute des sous-titres à une vidéo et génère une nouvelle vidéo avec les sous-titres.

    :param chemin_video: Chemin du fichier vidéo source.
    :param chemin_sous_titres: Chemin du fichier de sous-titres.
    :param chemin_sortie: Chemin du fichier vidéo de sortie.
    :param fontsize: Taille de la police des sous-titres.
    :param color: Couleur du texte des sous-titres.
    :param bg_color: Couleur de fond des sous-titres (None pour aucun fond).
    :param position: Position des sous-titres sur la vidéo.
    :param font: Police des sous-titres.
    """
    clip = VideoFileClip(chemin_video)
    subs = pysubs2.load(chemin_sous_titres)
    clips_sous_titres = []

    for sub in subs:
        debut = sub.start / 1000.0
        fin = sub.end / 1000.0
        texte = sub.text.replace('\n', ' ')
        
        if bg_color:
            texte_clip = TextClip(texte, fontsize=fontsize, color=color, bg_color=bg_color, font=font)
        else:
            texte_clip = TextClip(texte, fontsize=fontsize, color=color, font=font)
        
        texte_clip = texte_clip.set_position(('center', position)).set_duration(fin - debut).set_start(debut)
        clips_sous_titres.append(texte_clip)

    video_finale = CompositeVideoClip([clip] + clips_sous_titres)
    video_finale.write_videofile(chemin_sortie, codec='libx264', preset='fast')

    # Libérer les ressources
    clip.close()
    video_finale.close()