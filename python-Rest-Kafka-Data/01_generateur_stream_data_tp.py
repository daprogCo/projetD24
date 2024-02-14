import os

import random

import shutil
from flask import Flask, Response
from datetime import datetime

app= Flask(__name__)

DOSSIER_BASE = os.path.join(os.getcwd(), 'data', 'capteurs_data')
DOSSIER_SENT = os.path.join(DOSSIER_BASE, '_sent')
os.makedirs(DOSSIER_SENT, exist_ok=True)


def traiter_prochain_fichier():

    #Les fichiers du dossier (seulement json, et pas de DS_Store!)
    fichiers = [f for f in os.listdir(DOSSIER_BASE) if
                os.path.isfile(os.path.join(DOSSIER_BASE, f)) and f.endswith('.json')]
    if not fichiers:
        return "Aucun fichier de données à traiter.", 204

    #next file en ligne
    chemin_fichier = os.path.join(DOSSIER_BASE, fichiers[0])

    with open(chemin_fichier, 'r') as fichier:
        donnees = fichier.read()

    # Déplacez le fichier traité dans le dossier _sent
    shutil.move(chemin_fichier, os.path.join(DOSSIER_SENT, fichiers[0]))

    return donnees


@app.route('/sensordata')
def generate_data():
    donnees = traiter_prochain_fichier()
    print(donnees)


    timestamp='{}'.format(datetime.now().isoformat())
    temp_eau=str(round(random.uniform(10,35), 2))
    niveau_batt=str(round(random.uniform(10,12), 2))
    id=str(random.randint(1,99999))
    enregistrement = str(timestamp +' ' + temp_eau +' ' + niveau_batt +' '  + id)

    return Response(enregistrement, mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

