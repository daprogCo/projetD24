from kafka import KafkaConsumer
from json import loads
import base64
import requests
import json
from datetime import datetime

consumer = KafkaConsumer('datainput', bootstrap_servers=['localhost:9092'], auto_offset_reset='earliest', enable_auto_commit=True, consumer_timeout_ms=4000)

# Constantes
hbase_rest_url = "http://localhost:8080"
table_name = "data"
column_family = "main"
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Helper functions
def encode_base64(input_str):
    return base64.b64encode(input_str.encode()).decode()

def setData(data, row_key):
    return {
        "Row": [
            {
                "key": encode_base64(row_key),
                "Cell": [
                    {
                        "column": encode_base64(f"{column_family}:{qualifier}"),
                        "$": encode_base64(data[qualifier]),
                    } for qualifier in data
                ]
            }
        ]
    }

def sendRequest(data, row_key):
    url = f"{hbase_rest_url}/{table_name}/{row_key}"
    response = requests.put(url, data=json.dumps(data), headers=headers)
    if response.status_code == 201:
        print("Données ajoutées avec succès.")
        print(response)
    else:
        print(f"Erreur lors de l'ajout des données : {response.status_code}")

# Main function
def loadToHbase(data):
    event = loads(data)
    print(event)
    row_key  = f"{datetime.now().timestamp()}"
    load = setData(event, row_key)
    sendRequest(load, row_key)
    print("=" * 50)

# Create new table
url_create_table = f"{hbase_rest_url}/{table_name}/schema"
create_table = {
    "name": table_name,
    "ColumnSchema": [
        {
            "name": column_family
        }
    ]
}
response = requests.put(url_create_table, data=json.dumps(create_table), headers=headers)
if response.status_code == 200:
    print("Table créée avec succès.")
else:
    print(f"Erreur lors de la création de la table : {response.status_code}")

# Main loop
for message in consumer:
    data = message.value.decode('utf-8')
    print('Réception de données...')
    try:
        loadToHbase(data)
    except json.JSONDecodeError:
        print("Erreur de décodage JSON")
    except:
        print("Erreur inconnue")
