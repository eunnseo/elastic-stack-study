# from confluent_kafka import Consumer
# consumer = Consumer({
# 	'bootstrap.servers': 'localhost:9092',
# 	'group.id': 'console-consumer-37587',
# 	'default.topic.config': {
# 		'auto.offset.reset': 'smallest'
# 	}
# })

# consumer.subscribe(['bigdata'])
# while True:
# 	msg = consumer.poll(1.0)
# 	if msg is None:
# 		continue
# 	if msg.error():
# 		print("Consumer error: {}".format(msg.error()))
# 		continue
# 	print("Received message: {}".format(msg.value().decode("utf-8")))
# consumer.close()

#############################################

from kafka import KafkaConsumer
from json import loads

# topic, broker list
consumer = KafkaConsumer(
	'bigdata', # topic name
	bootstrap_servers=['localhost:9092'],
	auto_offset_reset='earliest',
	enable_auto_commit=True,
	group_id='my-group',
	value_deserializer=lambda x: loads(x.decode('utf-8')),
	consumer_timeout_ms=1000
)

# consumer list를 가져온다
print('[begin] get consumer list')
for message in consumer:
	print("Topic: %s, Partition: %d, Offset: %d, Key: %s, Value: %s" % ( message.topic, message.partition, message.offset, message.key, message.value ))
print('[end] get consumer list')
