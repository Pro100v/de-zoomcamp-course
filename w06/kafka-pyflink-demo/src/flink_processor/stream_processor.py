from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, TableDescriptor, Schema
from pyflink.common import Row
from pyflink.table.expressions import col, call, lit
from pyflink.table.window import Tumble

import src.common.config as config


def main():
    """Основная функция для запуска PyFlink стримингового процессора"""

    # Создание среды исполнения стримингового процесса
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)  #  Устанавливаем параллелизм в 1

    # Создание таблицы среды исполнения стриминга
    t_env = StreamTableEnvironment.create(env)

    # Добавление Kafka connector к таблице среды исполнения стриминга
    t_env.get_config().get_configuration().set_string(
        "pipeline.jars", config.FLINK_SQL_KAFKA_CONNECTORS_PATH
    )

    # Создание исходной таблицы для чтения данных из Kafka
    source_ddl = f"""
    CREATE TABLE sensor_data (
        sensor_id INT,
        temperature DOUBLE,
        humidity DOUBLE,
        timestamp STRING,
        event_time AS TO_TIMESTAMP(timestamp),
        WATERMARK FOR event_time AS event_time - INTERVAL '5' SECOND
    ) WITH (
        "connector" = 'kafka',
        "topic" = '{config.KAFKA_TOPIC_NAME}',
        "properties.bootstrap.servers" = '{config.KAFKA_BOOTSTRAP_SERVER}',
        "properties.group.id" = '{config.FLINK_GROUP_ID}',
        "scan.startup.mode" = 'earliest-offset',
        "format" = 'json',
        "json.fail-on-missing-field" = 'false',
        "json.ignore-parse-errors" = 'true'
    )
    """
    sink_ddl = f""" 
    CREATE TABLE temperature_averages (
        sensor_id INT,
        avg_temperature DOUBLE,
        window_start STRING,
        window_end STRING
    ) WITH (
            "connector" = 'kafka',
    "topic" = 'processed-topic',
    "properties.bootstrap.servers" = '{config.KAFKA_BOOTSTRAP_SERVER}',
    "format" = 'json',
    "json.fail-on-missing-field" = 'false',
    )
    """

    # Выполнение SQL DDL для создания таблиц
    t_env.execute_sql(source_ddl)
    t_env.execute_sql(sink_ddl)

    # SQL-запрос для вычисления средней температуры
    # Для каждого датчика за последние 1-минуту
    process_query = """
    INSERT INTO temperature_averages
    SELECT
        sensor_id,
        AVG(temperature) AS avg_temperature,
        DATE_FORMAT(TUMBLE_START(event_time, INTERVAL '1' MINUTE), 'yyyy-MM-dd HH:mm:ss') AS window_start,
        DATE_FORMAT(TUMBLE_END(event_time, INTERVAL '1' MINUTE), 'yyyy-MM-dd HH:mm:ss') AS window_end
    FROM sensor_data
    GROUP BY 
        sensor_id, 
        TUMBLE(event_time, INTERVAL '1' MINUTE)
    """

    # Выполнение SQL-запроса
    statement_set = t_env.create_statement_set()
    statement_set.add_insert_sql(process_query)
    job_client = statement_set.execute().get_job_client()

    # Ждем завершения работы (запустится асстнхронно)
    if job_client is not None:
        job_client.get_job_execution_result().result()


if __name__ == "__main__":
    main()
