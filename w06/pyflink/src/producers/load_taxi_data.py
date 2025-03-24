import csv
import time
import json
from kafka import KafkaProducer


def main():
    # Create a Kafka producer
    producer = KafkaProducer(
        bootstrap_servers="localhost:9092",
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    csv_file = (
        "data/green_tripdata_2019-10.csv"  # change to your CSV file path if needed
    )

    used_cols = [
        "lpep_pickup_datetime",
        "lpep_dropoff_datetime",
        "PULocationID",
        "DOLocationID",
        "passenger_count",
        "trip_distance",
        "tip_amount",
    ]
    try:
        with open(csv_file, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            print("Sending data to Kafka topic 'green-data'...")
            t0 = time.time()
            for row in reader:
                # Each row will be a dictionary keyed by the CSV headers
                # Send data to Kafka topic "green-data"
                row = {k: v for k, v in row.items() if k in used_cols}
                producer.send("green-data", value=row)

        # Make sure any remaining messages are delivered
        producer.flush()
        t1 = time.time()
        took = t1 - t0
        print(f"took {took:.2f} seconds")
    finally:
        producer.close()


if __name__ == "__main__":
    main()

