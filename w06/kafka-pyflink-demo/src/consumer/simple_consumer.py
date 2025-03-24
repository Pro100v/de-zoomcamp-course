from kafka import KafkaConsumer
import json

import src.common.config as config


def create_consumer():
    """Создание консьюмера Kafka"""
    consumer = KafkaConsumer(
        config.KAFKA_TOPIC_NAME,
        bootstrap_servers=[config.KAFKA_BOOTSTRAP_SERVER],
        auto_offset_reset="earliest",  # Начинаем с самого раннего сообщения
        enable_auto_commit=True,  # Автоматически фиксируем смещение
        group_id=config.KAFKA_CONSUMER_GROUP_ID,  #  Bыставляем идентификатор группы
        value_deserializer=lambda v: json.loads(v),
    )
    return consumer


def main():
    """Основная функция для запуска консьюмера"""
    consumer = create_consumer()
    try:
        print("Начинаем прослушивание топика...")
        for message in consumer:
            print(
                f"Получено сообщение из партиции: {message.partition}, смещение {message.offset}"
            )
            print(
                f"Ключ сообщения: {message.key.decode('utf-8') if message.key else None}"
            )
            print(f"Получено сообщение: {message.value}")
            print("-----")
    except KeyboardInterrupt:
        print("Остановка консьюмера...")
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
