from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import pysrt
import speech_recognition as sr

def extraire_audio(chemin_video, chemin_audio):
    clip = VideoFileClip(chemin_video)
    clip.audio.write_audiofile(chemin_audio)

def transcrire_audio(chemin_audio):
    recognizer = sr.Recognizer()
    with sr.AudioFile(chemin_audio) as source:
        audio = recognizer.record(source)
    texte = recognizer.recognize_google(audio, language='fr-FR')
    return texte

def generer_srt(texte_transcrit, chemin_srt, duree_video):
    sous_titres = pysrt.SubRipFile()
    mots = texte_transcrit.split()
    nb_mots = len(mots)
    duree_par_mot = duree_video / nb_mots

    for i, mot in enumerate(mots):
        debut = pysrt.SubRipTime(seconds=i * duree_par_mot)
        fin = pysrt.SubRipTime(seconds=(i + 1) * duree_par_mot)
        sous_titre = pysrt.SubRipItem(index=i+1, start=debut, end=fin, text=mot)
        sous_titres.append(sous_titre)

    sous_titres.save(chemin_srt, encoding='utf-8')

def ajouter_sous_titres(chemin_video, chemin_srt, chemin_sortie):
    clip = VideoFileClip(chemin_video)
    sous_titres = pysrt.open(chemin_srt)
    clips_sous_titres = []

    for sous_titre in sous_titres:
        debut = sous_titre.start.ordinal / 1000
        fin = sous_titre.end.ordinal / 1000
        texte = sous_titre.text.replace('\n', ' ')
        texte_clip = TextClip(texte, fontsize=24, color='white', bg_color='black')
        texte_clip = texte_clip.set_position(('center', 'bottom')).set_duration(fin - debut).set_start(debut)
        clips_sous_titres.append(texte_clip)

    video_finale = CompositeVideoClip([clip] + clips_sous_titres)
    video_finale.write_videofile(chemin_sortie, codec='libx264')

if __name__ == "__main__":
    chemin_video = "/home/dev/Bureau/video.mp4"
    chemin_audio = "audio_extrait.wav"
    chemin_srt = "sous_titres.srt"
    chemin_sortie = "video_avec_sous_titres.mp4"

    extraire_audio(chemin_video, chemin_audio)
    texte_transcrit = transcrire_audio(chemin_audio)
    clip = VideoFileClip(chemin_video)
    generer_srt(texte_transcrit, chemin_srt, clip.duration)
    ajouter_sous_titres(chemin_video, chemin_srt, chemin_sortie)