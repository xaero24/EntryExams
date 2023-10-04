from kafka import KafkaConsumer
from json import loads

consumer = KafkaConsumer(
   'test',
    bootstrap_servers = ['localhost : 9092'],  
    auto_offset_reset = 'earliest',  
    enable_auto_commit = True,  
    group_id = 'my-group',  
    value_deserializer = lambda x : loads(x.decode('utf-8'))  
    )

for m in consumer:
    print(m.value)