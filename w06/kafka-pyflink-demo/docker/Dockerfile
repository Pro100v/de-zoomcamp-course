FROM python:3.10-slim

# Установка UV и wget
RUN apt-get update && apt-get install -y wget && apt-get clean
RUN pip install uv

# # Альтернативная установка UV
# # The installer requires curl (and certificates) to download the release archive
# RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates
#
# # Download the latest installer
# ADD https://astral.sh/uv/install.sh /uv-installer.sh
#
# # Run the installer then remove it
# RUN sh /uv-installer.sh && rm /uv-installer.sh
#
# # Ensure the installed binary is on the `PATH`
# ENV PATH="/root/.local/bin/:$PATH"

# Создание директории для JAR-файлов Flink и загрузка коннектора
WORKDIR /opt/flink-connectors
# RUN wget https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-kafka/2.0.0/flink-sql-connector-kafka-2.0.0.jar
RUN wget https://repo1.maven.org/maven2/org/apache/flink/flink-sql-connector-kafka/3.4.0-1.20/flink-sql-connector-kafka-3.4.0-1.20.jar 
# Создание рабочей директории
WORKDIR /app

# Копирование файлов с зависимостями
COPY requirements.txt .

# Установка зависимостей с помощью UV
RUN uv pip install -r requirements.txt --system

# Копирование кода приложения
COPY ./src /app/src

# Команда запуска (будет переопределяться при запуске контейнера)
CMD ["python", "-m", "src.consumer.simple_consumer"]
