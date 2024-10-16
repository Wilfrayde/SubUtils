import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Ajouter le chemin du module au sys.path pour accéder aux modules à tester
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from align_subtitles_with_video import extraire_audio, transcrire_audio, segmenter_audio, generer_srt, ajouter_sous_titres

class TestSubtitleApp(unittest.TestCase):
    """
    Classe de test pour les fonctions de l'application de sous-titres.
    """

    def setUp(self):
        """
        Configuration initiale pour chaque test.
        Crée des chemins de fichiers de test et un fichier de sous-titres factice.
        """
        self.chemin_video = "test_video.mp4"
        self.chemin_audio = "test_audio.wav"
        self.chemin_srt = "test_subtitles.srt"
        self.chemin_sortie = "test_output.mp4"

        # Créer un fichier de sous-titres factice
        with open(self.chemin_srt, 'w') as f:
            f.write("1\n00:00:00,000 --> 00:00:01,000\nTest\n")

    def tearDown(self):
        """
        Nettoyage après chaque test.
        Supprime les fichiers de test créés.
        """
        for fichier in [self.chemin_audio, self.chemin_srt, self.chemin_sortie]:
            if os.path.exists(fichier):
                os.remove(fichier)

    @patch('align_subtitles_with_video.VideoFileClip')
    def test_extraire_audio(self, MockVideoFileClip):
        """
        Teste la fonction extraire_audio pour s'assurer que l'audio est extrait correctement.
        """
        mock_clip = MagicMock()
        mock_clip.audio = MagicMock()
        MockVideoFileClip.return_value = mock_clip
        extraire_audio(self.chemin_video, self.chemin_audio)
        mock_clip.audio.write_audiofile.assert_called_with(self.chemin_audio)

    @patch('align_subtitles_with_video.sr.AudioFile')
    @patch('align_subtitles_with_video.sr.Recognizer')
    def test_transcrire_audio(self, MockRecognizer, MockAudioFile):
        """
        Teste la fonction transcrire_audio pour s'assurer que l'audio est transcrit correctement.
        """
        mock_recognizer = MockRecognizer.return_value
        mock_audio_file = MockAudioFile.return_value
        mock_audio_file.__enter__.return_value = MagicMock()
        transcrire_audio(self.chemin_audio)
        mock_recognizer.record.assert_called()

    @patch('align_subtitles_with_video.AudioSegment.from_wav')
    @patch('align_subtitles_with_video.split_on_silence')
    def test_segmenter_audio(self, MockSplitOnSilence, MockAudioSegment):
        """
        Teste la fonction segmenter_audio pour s'assurer que l'audio est segmenté correctement.
        """
        mock_audio_segment = MagicMock()
        MockAudioSegment.return_value = mock_audio_segment
        segmenter_audio(self.chemin_audio)
        MockSplitOnSilence.assert_called_with(mock_audio_segment, min_silence_len=300, silence_thresh=mock_audio_segment.dBFS-16)

    @patch('align_subtitles_with_video.VideoFileClip')
    def test_generer_srt(self, MockVideoFileClip):
        """
        Teste la fonction generer_srt pour s'assurer que le fichier SRT est généré correctement.
        """
        texte = "Ceci est un test"
        segments = [b"segment1", b"segment2"]
        generer_srt(texte, self.chemin_srt, segments)
        self.assertTrue(os.path.exists(self.chemin_srt))

    @patch('align_subtitles_with_video.VideoFileClip')
    @patch('align_subtitles_with_video.TextClip')
    @patch('align_subtitles_with_video.CompositeVideoClip')
    def test_ajouter_sous_titres(self, MockCompositeVideoClip, MockTextClip, MockVideoFileClip):
        """
        Teste la fonction ajouter_sous_titres pour s'assurer que les sous-titres sont ajoutés correctement à la vidéo.
        """
        mock_clip = MagicMock()
        mock_clip.size = (640, 480)  # Assurez-vous que la taille est définie
        mock_clip.duration = 10.0  # Assurez-vous que la durée est définie
        MockVideoFileClip.return_value = mock_clip

        mock_text_clip = MagicMock()
        MockTextClip.return_value = mock_text_clip

        mock_composite_clip = MagicMock()
        MockCompositeVideoClip.return_value = mock_composite_clip

        ajouter_sous_titres(self.chemin_video, self.chemin_srt, self.chemin_sortie)
        mock_composite_clip.write_videofile.assert_called_with(self.chemin_sortie, codec='libx264', preset='fast')
        mock_clip.close.assert_called()

if __name__ == '__main__':
    unittest.main()