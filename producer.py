from kafka import KafkaProducer
from sensor_simulator import generate_weather_data, rand
import json
import time


BOOTSTRAP_SERVER = "lab9.alumchat.lol:9092"
TOPIC = "21699"

def kafka_producer() -> None:
    producer = KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVER,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )
    print(f"Sending data with topic {TOPIC} in {BOOTSTRAP_SERVER}")
    try:
        while True:
            data: dict = generate_weather_data()
            producer.send(TOPIC, data) 
            print(f"Topic: {TOPIC} Data: {data} sent")
            wait = rand.uniform(15, 30) # generate a wait between 15 and 30 secs
            time.sleep(wait)

    except KeyboardInterrupt:
        print("Producer stopped by user")
    except Exception as e:
        print(f"There was an error: {e}\n" \
              "If error suggests NoBrokersAvailable check server connection / availability")
    
    finally:
        producer.close()
