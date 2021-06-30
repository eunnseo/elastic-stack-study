from confluent_kafka import Consumer
consumer = Consumer({
	'bootstrap.servers': 'localhost:9092',
	'group.id': 'console-consumer-37587',
	'default.topic.config': {
		'auto.offset.reset': 'smallest'
	}
})

consumer.subscribe(['bigdata'])
while True:
	msg = consumer.poll(1.0)
	if msg is None:
		continue
	if msg.error():
		print("Consumer error: {}".format(msg.error()))
		continue
	print("Received message: {}".format(msg.value().decode("utf-8")))
consumer.close()
