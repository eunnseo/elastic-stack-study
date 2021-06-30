from confluent_kafka import Producer

producer = Producer({'bootstrap.servers': 'localhost:9092'})
for i in range(11):
    producer.poll(0)
    #(topic 이름, data 내용)
    producer.produce("bigdata", str(i).encode('utf-8'))
    print(str(i)+" is producing now")
    producer.flush() # flush - db commit 같은것!
