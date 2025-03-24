
## Модуль 2: Настройка тестовой среды с Docker и UV (обновленная структура)

### Обновленная структура проекта

```
kafka-pyflink-demo/
│
├── docker/
│   ├── docker-compose.yml    # Конфигурация для Kafka и ZooKeeper
│   └── Dockerfile            # Dockerfile для Python-приложения
│
├── requirements.txt          # Зависимости Python
│
└── src/
    ├── producer/
    │   ├── __init__.py
    │   └── simple_producer.py  # Код для публикации сообщений
    │
    ├── consumer/
    │   ├── __init__.py
    │   └── simple_consumer.py  # Простой консьюмер без использования Flink
    │
    └── flink_processor/
        ├── __init__.py
        └── stream_processor.py  # Обработка потока с PyFlink
```

### Шаг 1: Создание директорий проекта

Сначала создадим основную структуру директорий:

```bash
mkdir -p kafka-pyflink-demo/docker
mkdir -p kafka-pyflink-demo/src/producer
mkdir -p kafka-pyflink-demo/src/consumer
mkdir -p kafka-pyflink-demo/src/flink_processor
touch kafka-pyflink-demo/requirements.txt
```

### Шаг 2: Создание файла Docker Compose для Kafka

Создадим файл `kafka-pyflink-demo/docker/docker-compose.yml`:

```yaml
version: '3'
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    ports:
      - "2181:2181"

  kafka:
    image: confluentinc/cp-kafka:latest
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_AUTO_CREATE_TOPICS_ENABLE: "true"
```

### Шаг 3: Настройка Dockerfile для Python-приложения с UV

Создадим файл `kafka-pyflink-demo/docker/Dockerfile`:

```dockerfile
FROM python:3.10-slim

# Установка UV
RUN pip install uv

# Создание рабочей директории
WORKDIR /app

# Копирование файлов с зависимостями
COPY requirements.txt .

# Установка зависимостей с помощью UV
RUN uv pip install -r requirements.txt

# Копирование кода приложения
COPY ./src /app/src

# Команда запуска (будет переопределяться при запуске контейнера)
CMD ["python", "-m", "src.consumer.simple_consumer"]
```

### Шаг 4: Создание файла с зависимостями

Создадим файл `kafka-pyflink-demo/requirements.txt`:

```
kafka-python==2.0.2
apache-flink==1.16.1
pandas==2.0.0
```

### Шаг 5: Запуск и проверка кластера Kafka

Для запуска Kafka-кластера теперь используем обновленный путь к docker-compose.yml:

```bash
cd kafka-pyflink-demo
docker-compose -f docker/docker-compose.yml up -d
```

Для создания тестового топика:

```bash
docker compose -f docker/docker-compose.yml exec kafka kafka-topics --create --topic test-topic --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1

docker compose -f docker/docker-compose.yml exec kafka kafka-topics --create --topic processed-topic --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
```

### Шаг 6: Сборка и запуск Python-приложения с использованием Docker

Для создания образа Python-приложения:

```bash
cd kafka-pyflink-demo
docker build -t kafka-pyflink-app -f docker/Dockerfile .
```

Для запуска контейнера с приложением:

```bash
docker run --network host kafka-pyflink-app
```

Опция `--network host` позволит нашему приложению в контейнере обращаться к Kafka по адресу `localhost:9092`.

