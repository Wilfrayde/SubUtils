# Subtitle Application

Subtitle Application est une application GUI qui permet d'ajouter des sous-titres à une vidéo en utilisant la reconnaissance vocale.

## Fonctionnalités

- Extraction de l'audio d'une vidéo.
- Transcription de l'audio en texte.
- Segmentation de l'audio en fonction des silences.
- Génération de fichiers SRT.
- Ajout de sous-titres à la vidéo.

## Prérequis

- Python 3.6 ou supérieur
- `pip` pour installer les dépendances

## Installation

### Linux & Mac

1. Clonez le dépôt :

   ```bash
   git clone https://github.com/votre-utilisateur/subtitle-application.git
   cd subtitle-application
   ```

2. Créez un environnement virtuel et activez-le :

   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

3. Installez les dépendances :

   ```bash
   pip install -r requirements.txt
   ```

### Windows

1. Clonez le dépôt :

   ```bash
   git clone https://github.com/votre-utilisateur/subtitle-application.git
   cd subtitle-application
   ```

2. Créez un environnement virtuel et activez-le :

   ```bash
   python -m venv env
   .\env\Scripts\activate
   ```

3. Installez les dépendances :

   ```bash
   pip install -r requirements.txt
   ```

## Utilisation

1. Assurez-vous que votre environnement virtuel est activé.

2. Lancez l'application :

   ```bash
   python app.py
   ```

3. Utilisez l'interface pour sélectionner une vidéo, définir les options de sous-titres et générer la vidéo sous-titrée.

## Structure du Projet

- `app.py` : Point d'entrée de l'application.
- `src/ui_application.py` : Contient la logique de l'interface utilisateur.
- `src/align_subtitles_with_video.py` : Contient les fonctions pour traiter l'audio et les sous-titres.
- `test/test_subtitle_app.py` : Tests unitaires pour l'application.

## Contribuer

1. Forkez le projet.
2. Créez votre branche de fonctionnalité (`git checkout -b feature/AmazingFeature`).
3. Commitez vos modifications (`git commit -m 'Add some AmazingFeature'`).
4. Poussez vers la branche (`git push origin feature/AmazingFeature`).
5. Ouvrez une Pull Request.

## Problèmes Connus

- La reconnaissance vocale peut échouer si l'audio est de mauvaise qualité.
- Assurez-vous d'avoir une connexion Internet stable pour utiliser le service de reconnaissance vocale.

## Licence

Distribué sous la licence MIT.

## Remerciements

- [MoviePy](https://zulko.github.io/moviepy/) pour le traitement vidéo.
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) pour la reconnaissance vocale.
- [PyDub](https://github.com/jiaaro/pydub) pour le traitement audio.
- [PySubs2](https://github.com/tkarabela/pysubs2) pour la gestion des sous-titres.
