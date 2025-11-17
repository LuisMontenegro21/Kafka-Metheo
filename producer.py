from kafka import KafkaProducer
from sensor_simulator import generate_weather_data, rand
import json
import time



def kafka_producer(topic: str, bootstrap_server: str) -> None:
    producer = KafkaProducer(
        bootstrap_servers=bootstrap_server,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )
    print(f"Sending data with topic {topic} in {bootstrap_server}")
    try:
        while True:
            data: dict = generate_weather_data()
            producer.send(topic, data) 
            print(f"Topic: {topic} Data: {data} sent")
            wait = rand.uniform(15, 30) # generate a wait between 15 and 30 secs
            time.sleep(wait)

    except KeyboardInterrupt:
        print("Producer stopped by user")
    except Exception as e:
        print(f"There was an error: {e}\n" \
              "If error suggests NoBrokersAvailable check server connection / availability")
    
    finally:
        producer.close()
