from kafka import KafkaProducer
import json
import time
import random
from datetime import datetime

import src.common.config as config


def create_producer():
    producer = KafkaProducer(
        bootstrap_servers=[config.KAFKA_BOOTSTRAP_SERVER],
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )
    return producer


def generate_sensor_data():
    """Генерация имитационных данных датчика"""

    return {
        "sensor_id": random.randint(1, 5),
        "temperature": round(random.uniform(15.0, 35.0), 2),
        "humidity": round(random.uniform(30, 90), 2),
        "timestamp": datetime.now().isoformat(),
    }


def main():
    """Основная функция для запуска продуцера"""

    producer = create_producer()
    topic_name = config.KAFKA_TOPIC_NAME

    try:
        while True:
            # Генерация данных датчика
            data = generate_sensor_data()
            # Определяем ключ сообщения на основе sensor_id
            key = str(data["sensor_id"]).encode("utf-8")
            future = producer.send(topic_name, value=data, key=key)
            # Ожидание публикации сообщения
            record_metadata = future.get(timeout=10)
            print(
                f"Сообщение отправлено в топик {record_metadata.topic!r}, "
                f"партиция {record_metadata.partition!r}, "
                f"с смещением {record_metadata.offset!r}"
            )
            print(f"Sent: {data}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Остановка продюсера...")
    finally:
        producer.close()


if __name__ == "__main__":
    main()
