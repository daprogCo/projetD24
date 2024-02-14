from kafka import KafkaConsumer

consumer= KafkaConsumer('sensordatainputfrancois', bootstrap_servers=['localhost:9092'], auto_offset_reset='earliest', enable_auto_commit=True, consumer_timeout_ms=1000)


def get_topic_data(dataraw):
    print("hello")
    print(dataraw)
    token= dataraw.split()
    print('Timestamp:{}'.format(token[0]))
    print('Temperature:{}'.format(token[1]))
    print('Niveau batterie:{}'.format(token[2]))
    # print('Id:{}'.format(token[3]))
    print('='* 50)

def get_topic_data2v2(dataraw):
    print('get_topic_data2v2:{}'.format(dataraw))
    print(dataraw)
    tokenb= dataraw.split()
    print(len(tokenb))
    tokenb_copy = tokenb.copy()
    print(len(tokenb_copy))

    # moi=tokenb
    # print(tokenb_copy[0])
    # print(tokenb[0])
    # print('Temperature:{}'.format(tokenb[1]))
    # print('Niveau batterie:{}'.format(tokenb[2]))


for message in consumer:
    data=message.value.decode('utf-8')
    print('Reception de data...')
    get_topic_data2v2(data)
    print(data)
