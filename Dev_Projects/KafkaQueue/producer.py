from kafka import KafkaProducer
from json import dumps
from time import sleep

producer = KafkaProducer(
    bootstrap_servers = ['localhost:9092'],  
    value_serializer = lambda x:dumps(x).encode('utf-8')  
    )

for i in range(500):
    producer.send("test", value={f"hello at index {i}": "producer"})
    sleep(1)