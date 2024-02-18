import requests
import base64
import json

# Encodage en Base64
def encode_base64(input_str):
    return base64.b64encode(input_str.encode()).decode()

# Adresse du serveur HBase REST et nom de la table
hbase_rest_url = 'http://localhost:8080'
table_name = 'data'
row_key = 'maligne1'
column_family = 'main'
qualifier = 'macolonne'
qualifier2 = 'macolonne2'
value = 'foufoutre'

# Construction de l'URL pour l'opération PUT
url = f"{hbase_rest_url}/{table_name}/{row_key}"

# Préparation des données pour l'envoi
data = {
    "Row": [
        {
            "key": encode_base64(row_key),
            "Cell": [
                {
                    "column": encode_base64(f"{column_family}:{qualifier}"),
                    "$": encode_base64(value),
                },
                {
                    "column": encode_base64(f"{column_family}:{qualifier2}"),
                    "$": encode_base64(value),
                }
            ]
        }
    ]
}

# En-têtes de la requête
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Envoi de la requête PUT
response = requests.put(url, data=json.dumps(data), headers=headers)

# Vérification du résultat
if response.status_code == 200:
    print("Données ajoutées avec succès.")
    print(response)
else:
    print(f"Erreur lors de l'ajout des données : {response.status_code}")
