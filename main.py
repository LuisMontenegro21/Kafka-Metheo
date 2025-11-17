from producer import kafka_producer
from consumer import kafka_consumer
import sys

def main() -> None:
    BOOTSTRAP_SERVER = "iot.redesuvg.cloud:9092"
    TOPIC = "21699"
    val = sys.argv[1]
    mode = sys.argv[2]
    if val == "produce":
        kafka_producer(topic=TOPIC, bootstrap_server=BOOTSTRAP_SERVER, mode=mode)
    elif val == "consume":
        kafka_consumer(topic=TOPIC, bootstrap_server=BOOTSTRAP_SERVER, mode=mode)
    else:
        print("Not a valid argument: use 'produce' and 'consume' only")

if __name__ == '__main__':
    main()