from kafka import KafkaConsumer
import json

def kafka_consumer(topic: str, bootstrap_server: str) -> tuple[list, list, list]:

    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_server,
        group_id="lp-gc-group",
        auto_offset_reset="earliest",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    )
    all_temp: list = []
    all_hum: list = []
    all_wind: list = []
    for message in consumer:
        print("Received:", message)
        all_temp.append(message['temperatura'])
        all_hum.append(message['humedad'])
        all_wind.append(message['direccion_viento'])
    
    return all_temp, all_hum, all_wind

