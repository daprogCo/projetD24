from kafka import KafkaConsumer
from json import loads

consumer = KafkaConsumer('datainput', bootstrap_servers=['localhost:9092'], auto_offset_reset='earliest', enable_auto_commit=True, consumer_timeout_ms=4000)

def get_topic_data(data):
    try:
        data = loads(data)
        for key, value in data.items():
            print(f'{key}: {value}')
    except:
        print(data)
    print("=" * 50)

for message in consumer:
    data = message.value.decode('utf-8')
    print('Réception de données...')
    response = get_topic_data(data)