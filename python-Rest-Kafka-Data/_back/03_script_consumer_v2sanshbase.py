from kafka import KafkaConsumer
import json
import sqlite3


########################################################################################
######    CONST
LOG_bLOG = True  #logguer chaque entrées\save
DB_bCLEANDB = True #Vider la table à chaque load du script



########################################################################################
######    DATABASE

class DatabaseManager:
    def __init__(self, db_name, clean_start=False):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.conn.execute('''CREATE TABLE IF NOT EXISTS events
                             (time TEXT, customer TEXT, action TEXT, device TEXT)''')
        self.conn.commit()

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
######    CONSUMER

consumer = KafkaConsumer('sensordatainputfrancois', bootstrap_servers=['localhost:9092'], auto_offset_reset='earliest', enable_auto_commit=True, consumer_timeout_ms=1000)



for message in consumer:
    data = message.value.decode('utf-8')
    try:
        events = json.loads(data)
        for event in events:
            db_manager.insert_event(event)
            if LOG_bLOG :
                print(f"Saved to DB - Time: {event['time']}, Customer: {event['customer']}, Action: {event['action']}, Device: {event['device']}")

    except json.JSONDecodeError:
        print("Erreur de décodage JSON")
