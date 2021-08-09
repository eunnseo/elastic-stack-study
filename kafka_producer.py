# from confluent_kafka import Producer

# producer = Producer({'bootstrap.servers': 'localhost:9092'})
# for i in range(11):
#     producer.poll(0)
#     #(topic 이름, data 내용)
#     producer.produce("bigdata", str(i).encode('utf-8'))
#     print(str(i)+" is producing now")
#     producer.flush() # flush - db commit 같은것!

#############################################

from kafka import KafkaProducer
from json import dumps
import time

producer = KafkaProducer(acks=0, compression_type='gzip', bootstrap_servers=['localhost:9092'], value_serializer=lambda x: dumps(x).encode('utf-8'))

start = time.time()
for i in range(10):
    data = {'str' : 'result' + str(i)}
    producer.send('bigdata', value=data) # topic name: bigdata, value: data
    producer.flush()
print("elapsed :", time.time() - start)
