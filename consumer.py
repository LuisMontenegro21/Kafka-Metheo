from kafka import KafkaConsumer
import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from encoding import decode


def kafka_consumer(topic: str, bootstrap_server: str, mode: str="json") -> None:
    consumer : KafkaConsumer
    if mode == 'json':
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_server,
            group_id="lp-gc-group",
            auto_offset_reset="earliest",
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        )
    elif mode == 'bytes':
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_server,
            group_id="lp-gc-group",
            auto_offset_reset="earliest",
            value_deserializer=lambda m: m,
        )
    else:
        raise ValueError("mode has to be 'bytes' or 'json'")
    all_temp: list = []
    all_hum: list = []
    # all_wind: list = []
    
    plt.style.use("seaborn-v0_8")
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8,6))


    def update(frame):
        records = consumer.poll(timeout_ms=200)
        if not records:
            return

        for tp, batch in records.items():
            for msg in batch:
                raw = msg.value   
                if mode == 'json':
                    data = raw
                else: 
                    if len(raw) != 3:
                        print(f"Skipping payload with len={len(raw)}: {raw!r}")
                        continue
                    try:
                        data = decode(raw)
                    except ValueError as e:
                        print(f"Decode error: {e} payload={raw!r}")
                        continue
                temp = data.get("temperatura")
                hum = data.get("humedad")

                
                if temp is None or hum is None:
                    continue

                all_temp.append(temp)
                all_hum.append(hum)


        if not all_temp:
            return
        window_size = 30
        temps_window = all_temp[-window_size:]
        hums_window = all_hum[-window_size:]

        ax1.clear()
        ax1.plot(temps_window)
        ax1.set_ylim(0, 120)
        ax1.set_ylabel("Temperatura")
        ax1.set_title("Temperatura (últimas lecturas)")

        ax2.clear()
        ax2.plot(hums_window)
        ax2.set_ylim(0, 100)
        ax2.set_ylabel("Humedad")
        ax2.set_title("Humedad (últimas lecturas)")
        
    ax1.set_title("Temperatura")
    ax1.set_ylim(0, 120)

    ax2.set_title("Humedad")
    ax2.set_ylim(0, 100)

    ani = animation.FuncAnimation(fig, update, interval=1000)
    plt.tight_layout()
    plt.show()


