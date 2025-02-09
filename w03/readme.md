# Module 3 Homework
<!-- markdownlint-disable MD013, MD041, MD033 -->

All bash commands run into `./w03` directory.

## Prepare date

### Upload data to GCS

### Create external table

1. Run `bq` CLI command to define options for external table. Definition stored in `./hw/ext_table_def.json` file.

```bash
bq mkdef --source_format=PARQUET \
   'gs://de-student-zoomcamp-probe/hw03/yellow_tripdata_2024-*.parquet' \
 > ./hw/ext_table_def.json
```

- <details>
  <summary><i>hw/ext_table_def.json</i></summary>
  
  ```json
    {
      "parquetOptions": {
        "enableListInference": false,
        "enumAsString": false,
        "mapTargetType": null
      },
      "sourceFormat": "PARQUET",
      "sourceUris": [
        "gs://de-student-zoomcamp-probe/hw03/yellow_tripdata_2024-*.parquet"
      ]
    }
  ```
  
</details>

2. Execute script for creating external BQ table from definition below.

```bash
bq mk --external_table_definition=./hw/ext_table_def.json \
   zoomcamp.hw03_external_yellow_tripdata
```

### Create native table

To create native BQ table run this command

- <details>
  <summary><i>./hw/00_create_native_table.sql</i></summary>
  
  ```sql
  CREATE OR REPLACE TABLE terraform-probe-448818.zoomcamp.hw03_native_yellow_tripdata AS
  SELECT * FROM `terraform-probe-448818.zoomcamp.hw03_external_yellow_tripdata`
  ```
  
</details>

```bash
cat ./hw/00_create_native_table.sql | bq query --use_legacy_sql=false
```

## Questions

### Question 1

#### Statement

What is count of records for the 2024 Yellow Taxi Data?

- 65,623
- 840,402
- 20,332,093
- 85,431,289

#### Solution

- <details>
  <summary><i>hw/01.sql</i></summary>
  
  ```sql
  select count(*) from zoomcamp.hw03_external_yellow_tripdata 
  ```
  
</details>

```bash
cat hw/01.sql | bq query --use_legacy_sql=false
+----------+
|   f0_    |
+----------+
| 20332093 |
+----------+
```

**Answer** is:

- 20,332,093

### Questions 2

#### Statement

Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables.</br>
What is the **estimated amount** of data that will be read when this query is executed on the External Table and the Table?

- 18.82 MB for the External Table and 47.60 MB for the Materialized Table
- 0 MB for the External Table and 155.12 MB for the Materialized Table
- 2.14 GB for the External Table and 0MB for the Materialized Table
- 0 MB for the External Table and 0MB for the Materialized Table

#### Solution

SQL scripts for solving question.

- <details>
  <summary><i>hw/02_ext.sql</i></summary>
  
  ```sql
  SELECT DISTINCT PULocationID
    FROM terraform-probe-448818.zoomcamp.hw03_external_yellow_tripdata;

  ```
  
</details>

- <details>
  <summary><i>hw/02_nat.sql</i></summary>
  
  ```sql

  SELECT DISTINCT PULocationID
    FROM terraform-probe-448818.zoomcamp.hw03_native_yellow_tripdata;
  ```
  
</details>

1. Command for estimate query for external table.

```bash
cat hw/02_ext.sql | bq query --use_legacy_sql=false --dry_run
> Query successfully validated. Assuming the tables are not modified, running this query will process lower bound of 0 bytes of data.
```

2. Command for estimate query for native table.

```bash
cat hw/02_nat.sql | bq query --use_legacy_sql=false --dry_run
> Query successfully validated. Assuming the tables are not modified, running this query will process 162656744 bytes of data.
```

**Answer** is:

- 0 MB for the External Table and 155.12 MB for the Materialized Table

### Question 3

#### Statement

Write a query to retrieve the PULocationID from the table (not the external table) in BigQuery. Now write a query to retrieve the PULocationID and DOLocationID on the same table. Why are the estimated number of Bytes different?

- BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires
reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.
- BigQuery duplicates data across multiple storage partitions, so selecting two columns instead of one requires scanning the table twice,
doubling the estimated bytes processed.
- BigQuery automatically caches the first queried column, so adding a second column increases processing time but does not affect the estimated bytes scanned.
- When selecting multiple columns, BigQuery performs an implicit join operation between them, increasing the estimated bytes processed

#### Solution

SQL script for solving question.

- <details>
  <summary><i>hw/03.sql</i></summary>
  
  ```sql
  SELECT DISTINCT PULocationID, DOLocationID
    FROM terraform-probe-448818.zoomcamp.hw03_external_yellow_tripdata;

  ```
  
</details>

Result for select a one column is presented in previous solution section. Result for select two columns is presented below

```bash
cat hw/03.sql | bq query --use_legacy_sql=false --dry_run
> Query successfully validated. Assuming the tables are not modified, running this query will process 325313488 bytes of data.
```

I think, that correct **answer** in this statement:

- BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires

### Question 4

#### Statement

How many records have a fare_amount of 0?

- 128,210
- 546,578
- 20,188,016
- 8,333

#### Solution

- <details>
  <summary><i>hw/04.sql</i></summary>
  
  ```sql
  SELECT count(*)
    FROM terraform-probe-448818.zoomcamp.hw03_native_yellow_tripdata
  WHERE fare_amount=0;
  ```
  
</details>

```bash
cat hw/04.sql | bq query --use_legacy_sql=false
+------+
| f0_  |
+------+
| 8333 |
+------+
```

**Answer** is:

- 8,333

### Question 5

#### Statement

What is the best strategy to make an optimized table in Big Query if your query will always filter based on tpep_dropoff_datetime and order the results by VendorID (Create a new table with this strategy)

- Partition by tpep_dropoff_datetime and Cluster on VendorID
- Cluster on by tpep_dropoff_datetime and Cluster on VendorID
- Cluster on tpep_dropoff_datetime Partition by VendorID
- Partition by tpep_dropoff_datetime and Partition by VendorID

#### Solution

I think that the best solution is the first proposal:

- **Partition by tpep_dropoff_datetime and Cluster on VendorID**
- 2nd proposal not good because partitioned by datetime column is better for cost querying.
- 3rd proposal not good because partitioned by VendorID make many small sized table ant this is looked is not efficient.
- 4th proposal is wrong because partitioned must be only one column.

- <details>
  <summary><i>hw/05.sql</i></summary>
  
  ```sql
  CREATE OR REPLACE TABLE terraform-probe-448818.zoomcamp.hw03_05_native_yellow_tripdata
    PARTITION BY DATE(tpep_dropoff_datetime)
    CLUSTER BY VendorID
    AS
    SELECT * FROM terraform-probe-448818.zoomcamp.hw03_external_yellow_tripdata
  ```
  
</details>

```bash
cat hw/05.sql | bq query --use_legacy_sql=false
> Waiting on bqjob_r6772b26b047143b4_00000194ec8060b9_1 ... (15s) Current status: DONE   
> Created terraform-probe-448818.zoomcamp.hw03_05_native_yellow_tripdata
```

### Question 6

#### Statement

Write a query to retrieve the distinct VendorIDs between tpep_dropoff_datetime
2024-03-01 and 2024-03-15 (inclusive)</br>

Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 5 and note the estimated bytes processed. What are these values? </br>

Choose the answer which most closely matches.</br>

- 12.47 MB for non-partitioned table and 326.42 MB for the partitioned table
- 310.24 MB for non-partitioned table and 26.84 MB for the partitioned table
- 5.87 MB for non-partitioned table and 0 MB for the partitioned table
- 310.31 MB for non-partitioned table and 285.64 MB for the partitioned table

#### Solution

SQL scripts for solving question.

- <details>
  <summary><i>./hw/06_non_partition.sql</i></summary>
  
  ```sql
  SELECT DISTINCT VendorID 
    FROM terraform-probe-448818.zoomcamp.hw03_native_yellow_tripdata
    where tpep_dropoff_datetime between '2024-03-01' and '2024-03-15';

  ```
  
</details>

- <details>
  <summary><i>./hw/o6_partition.sql</i></summary>
  
  ```sql
  SELECT DISTINCT VendorID 
    FROM terraform-probe-448818.zoomcamp.hw03_05_native_yellow_tripdata
    where tpep_dropoff_datetime between '2024-03-01' and '2024-03-15';

  ```
  
</details>

1. Command for estimate query for non-partitioned table.

```bash
cat ./hw/06_non_partition.sql | bq query --use_legacy_sql=false --dry_run
> Query successfully validated. Assuming the tables are not modified, running this query will process 325313488 bytes of data.
```

2. Command for estimate query for partitioned table.

```bash
cat ./hw/o6_partition.sql | bq query --use_legacy_sql=false --dry_run
> Query successfully validated. Assuming the tables are not modified, running this query will process upper bound of 28141776 bytes of data.
```

**Answer** is:

- 310.24 MB for non-partitioned table and 26.84 MB for the partitioned table

### Question 7

#### Statement

Where is the data stored in the External Table you created?

- Big Query
- Container Registry
- GCP Bucket
- Big Table

#### Solution

**Answer** is:

- GCP Bucket

### Question 8

#### Statement

It is best practice in Big Query to always cluster your data:

- True
- False

#### Solution

**Answer** is:

- False
