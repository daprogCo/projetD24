from kafka import KafkaConsumer
import json
import sqlite3
import requests
import base64  



########################################################################################
######    CONST
LOG_bLOG = True  #logguer chaque entrées\save
DB_bCLEANDB = True #Vider la table à chaque load du script



########################################################################################
######    HELPERS

def encode_base64(input_str):
    return base64.b64encode(input_str.encode()).decode()


########################################################################################
######    DATABASE SQLITE

class DatabaseManager:
    def __init__(self, db_name, clean_start=False):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.conn.execute('''CREATE TABLE IF NOT EXISTS events
                             (time TEXT, customer TEXT, action TEXT, device TEXT)''')
        self.conn.commit()
        if clean_start:   #Petit utils pour nettoyer ma table à chaque load du script
            self.clean_table()

    def insert_event(self, event):
        self.conn.execute("INSERT INTO events (time, customer, action, device) VALUES (?, ?, ?, ?)",
                          (event['time'], event['customer'], event['action'], event['device']))
        self.conn.commit()

    def clean_table(self):
        self.conn.execute('DELETE FROM events')
        self.conn.commit()
    def close(self):
        self.conn.close()


db_manager = DatabaseManager('data/consumer.db', DB_bCLEANDB)


########################################################################################
######    DATABASE HBASE

class HBaseManager:
    def __init__(self, hbase_rest_url, table_name):
        self.hbase_rest_url = hbase_rest_url
        self.table_name = table_name
        if self.checkIf_table_exists() == False:
            self.create_table()


    def checkIf_table_exists(self):
        #http://localhost:8080/events/schema
        url = f"{self.hbase_rest_url}/{self.table_name}/schema"
        maReponse = requests.get(url)
        if maReponse.status_code == 200:
            print("Table already exists in HBase.")
            return True

        else:
            print(f"Table does not exist in HBase: {maReponse.status_code}")
            return False

    def create_table(self):
        #ref: https://docs.cloudera.com/runtime/7.2.17/accessing-hbase/topics/hbase-using-the-rest-api.html (/table/schema)
        url = f"{self.hbase_rest_url}/{self.table_name}/schema"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        data = {
            "name": self.table_name,
            "ColumnSchema": [
                {
                    "name": "info"  # le nom de ma colonne family
                }
            ]
        }
        maReponse = requests.post(url, data=json.dumps(data), headers=headers)
        if maReponse.status_code == 201:
            print("Table successfully created in HBase.")
        else:
            print(f"Error creating table in HBase: {maReponse.status_code}")
            
            
            
            

    def insert_event(self, row_key, data):

        url = f"{self.hbase_rest_url}/{self.table_name}/{row_key}"
        
        formatted_data = {
            "Row": [
                {
                    "key": encode_base64(row_key),
                    "Cell": [
                        {
                            "column": encode_base64(f"info:{qualifier}"),
                            "$": encode_base64(data[qualifier]),
                        } for qualifier in data
                    ]
                }
            ]
        }

        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        maReponse = requests.put(url, data=json.dumps(formatted_data), headers=headers)
        
        if maReponse.status_code == 200:
            if LOG_bLOG:
                print("Data successfully added to HBase.")
        else:
            if LOG_bLOG:
                print(f"Error adding data to HBase: {maReponse.status_code}")



hbase_manager = HBaseManager('http://localhost:8080', 'events')


########################################################################################
######    CONSUMER

consumer = KafkaConsumer('sensordatainputfrancois', bootstrap_servers=['localhost:9092'], auto_offset_reset='earliest', enable_auto_commit=True, consumer_timeout_ms=1000)



for message in consumer:
    data = message.value.decode('utf-8')
    try:
        events = json.loads(data)
        for event in events:
            db_manager.insert_event(event)

            row_key = f"{event['customer']}_{event['time']}"
            hbase_manager.insert_event(row_key, event)
            
            
            
            if LOG_bLOG :
                print(f"Saved to DB - Time: {event['time']}, Customer: {event['customer']}, Action: {event['action']}, Device: {event['device']}")

    except json.JSONDecodeError:
        print("Erreur de décodage JSON")
