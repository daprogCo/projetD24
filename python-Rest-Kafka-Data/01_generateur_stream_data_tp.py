import os

import random
import json

import shutil
from flask import Flask, Response
from datetime import datetime

app= Flask(__name__)




########################################################################################
######    GESTION FICHIERS

DOSSIER_BASE = os.path.join(os.getcwd(), 'data', 'capteurs_data')
DOSSIER_SENT = os.path.join(DOSSIER_BASE, '_sent')
os.makedirs(DOSSIER_SENT, exist_ok=True)


def traiter_prochain_fichier():
    fichiers = [f for f in os.listdir(DOSSIER_BASE) if
                os.path.isfile(os.path.join(DOSSIER_BASE, f)) and f.endswith('.json')]
    if not fichiers:
        return "Aucun fichier de données à traiter.", 204

    chemin_fichier = os.path.join(DOSSIER_BASE, fichiers[0])

    with open(chemin_fichier, 'r') as fichier:
        donnees = json.load(fichier)

    shutil.move(chemin_fichier, os.path.join(DOSSIER_SENT, fichiers[0]))
    return json.dumps(donnees)


def resetFiles():
    # Vérifie si le dossier _sent contient des fichiers
    if os.path.exists(DOSSIER_SENT):
        fichiers = os.listdir(DOSSIER_SENT)
        for fichier in fichiers:
            chemin_source = os.path.join(DOSSIER_SENT, fichier)
            chemin_destination = os.path.join(DOSSIER_BASE, fichier)
            shutil.move(chemin_source, chemin_destination)
        print("Tous les fichiers ont été replacés dans le dossier de base.")
    else:
        print("Le dossier _sent n'existe pas.")



########################################################################################
######    ROUTES
@app.route('/sensordata')
def generate_data():
    donnees = traiter_prochain_fichier()
    return Response(donnees, mimetype='application/json')






if __name__ == '__main__':
    resetFiles()
    app.run(host='0.0.0.0', debug=True)

