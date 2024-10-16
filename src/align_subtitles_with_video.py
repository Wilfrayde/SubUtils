from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import pysubs2
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os

def extraire_audio(chemin_video, chemin_audio):
    clip = VideoFileClip(chemin_video)
    clip.audio.write_audiofile(chemin_audio)

def transcrire_audio(chemin_audio):
    recognizer = sr.Recognizer()
    with sr.AudioFile(chemin_audio) as source:
        audio = recognizer.record(source)
    texte = recognizer.recognize_google(audio, language='fr-FR')
    return texte

def segmenter_audio(chemin_audio):
    audio = AudioSegment.from_wav(chemin_audio)
    segments = split_on_silence(audio, min_silence_len=300, silence_thresh=audio.dBFS-16)
    return segments

def generer_srt(texte_transcrit, chemin_srt, segments):
    subs = pysubs2.SSAFile()
    mots = texte_transcrit.split()
    index_mot = 0
    total_mots = len(mots)

    for i, segment in enumerate(segments):
        debut = sum(len(s) for s in segments[:i]) / 1000.0
        fin = debut + len(segment) / 1000.0
        nb_mots_segment = int((len(segment) / sum(len(s) for s in segments)) * total_mots)
        texte_segment = ' '.join(mots[index_mot:index_mot + nb_mots_segment])
        index_mot += nb_mots_segment
        subs.append(pysubs2.SSAEvent(start=pysubs2.make_time(s=debut), end=pysubs2.make_time(s=fin), text=texte_segment))

    subs.save(chemin_srt, encoding='utf-8')

def ajouter_sous_titres(chemin_video, chemin_sous_titres, chemin_sortie, fontsize=24, color='white', bg_color=None, position='bottom', font='Arial'):
    clip = VideoFileClip(chemin_video)
    subs = pysubs2.load(chemin_sous_titres)
    clips_sous_titres = []

    for sub in subs:
        debut = sub.start / 1000.0
        fin = sub.end / 1000.0
        texte = sub.text.replace('\n', ' ')
        
        # Créer le TextClip sans bg_color si bg_color est None
        if bg_color:
            texte_clip = TextClip(texte, fontsize=fontsize, color=color, bg_color=bg_color, font=font)
        else:
            texte_clip = TextClip(texte, fontsize=fontsize, color=color, font=font)
        
        texte_clip = texte_clip.set_position(('center', position)).set_duration(fin - debut).set_start(debut)
        clips_sous_titres.append(texte_clip)

    video_finale = CompositeVideoClip([clip] + clips_sous_titres)
    video_finale.write_videofile(chemin_sortie, codec='libx264')