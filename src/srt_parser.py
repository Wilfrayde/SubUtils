import pysrt

def analyser_srt(chemin_fichier_srt):
    # Charger le fichier SRT
    sous_titres = pysrt.open(chemin_fichier_srt)
       
    # Parcourir chaque sous-titre
    for sous_titre in sous_titres:
        # Extraire le texte et les timings
        debut = sous_titre.start.to_time()
        fin = sous_titre.end.to_time()
        texte = sous_titre.text
           
        # Afficher les informations
        print(f"Début: {debut}, Fin: {fin}, Texte: {texte}")
    