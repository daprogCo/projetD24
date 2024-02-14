import time

import requests
from kafka import KafkaProducer

producer= KafkaProducer(bootstrap_servers=['localhost:9092'])

def get_sensor_data():
        try:
            url= 'http://127.0.0.1:5000/sensordata'
            data=requests.get(url)
            return data.text

        except:
            return 'Erreur de connection server(fh)'


while True:
    message = get_sensor_data()
    print ('Sending data to the topic...')
    producer.send('sensordatainputfrancois', message.encode('utf-8'))
    time.sleep(3)



