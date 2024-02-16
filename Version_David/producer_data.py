from kafka import KafkaProducer
import time
import requests

producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

def get_sensor_data(file, line):
    try:
        url = f"http://127.0.0.1:5000/data/{file}/{line}"
        data = requests.get(url)
        return data.text
    except:
        return "error"

for f in range(1, 21):
    for l in range(1000):
        message = get_sensor_data(f, l)
        print("Sending data ...")
        producer.send('datainput', message.encode('utf-8'))
        time.sleep(3)