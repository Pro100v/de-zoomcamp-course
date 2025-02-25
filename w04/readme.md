# Module 4 Homework

## Prepare date

There is changed Kestra Flow to upload source data from github.com to GCS:

- in the flow parameters add option `subdir` (optional) that upload data
into sub directory in the bucket (to isolate data per module homework)
- add files template to each source type (more robust logic)

Source of flow [./flows/flow.yaml](./flows/flow.yaml)

Checks data after upload.

```sql
select 'Green data' as tab_name, count(*) from `terraform-probe-448818.zoomcamp.hw04-green-raw`
union all
select 'Yellow data' as tab_name, count(*) from `terraform-probe-448818.zoomcamp.hw04-yellow-raw`
union all
select 'FHV data' as tab_name, count(*) from `terraform-probe-448818.zoomcamp.hw04_fhv_raw`;
```

|tab_name     |count       |
|:--------    |     ------:|
|Green data   |     7778101|
|Yellow data  |   109047518|
|FHV data     |    43244696|

## Questions

### Question 1: Understanding dbt model resolution

Provided you've got the following sources.yaml

```yaml
version: 2

sources:
  - name: raw_nyc_tripdata
    database: "{{ env_var('DBT_BIGQUERY_PROJECT', 'dtc_zoomcamp_2025') }}"
    schema:   "{{ env_var('DBT_BIGQUERY_SOURCE_DATASET', 'raw_nyc_tripdata') }}"
    tables:
      - name: ext_green_taxi
      - name: ext_yellow_taxi
```

with the following env variables setup where `dbt` runs:

```shell
export DBT_BIGQUERY_PROJECT=myproject
export DBT_BIGQUERY_DATASET=my_nyc_tripdata
```

What does this .sql model compile to?

```sql
select * 
from {{ source('raw_nyc_tripdata', 'ext_green_taxi' ) }}
```

- `select * from dtc_zoomcamp_2025.raw_nyc_tripdata.ext_green_taxi`
- `select * from dtc_zoomcamp_2025.my_nyc_tripdata.ext_green_taxi`
- **`select * from myproject.raw_nyc_tripdata.ext_green_taxi`**
- `select * from myproject.my_nyc_tripdata.ext_green_taxi`
- `select * from dtc_zoomcamp_2025.raw_nyc_tripdata.green_taxi`

### Question 2: dbt Variables & Dynamic Models

Say you have to modify the following dbt_model (`fct_recent_taxi_trips.sql`) to enable Analytics Engineers
to dynamically control the date range.

- In development, you want to process only **the last 7 days of trips**
- In production, you need to process **the last 30 days** for analytics

```sql
select *
from {{ ref('fact_taxi_trips') }}
where pickup_datetime >= CURRENT_DATE - INTERVAL '30' DAY
```

What would you change to accomplish that in a such way that command line arguments takes precedence
over ENV_VARs, which takes precedence over DEFAULT value?

- Add `ORDER BY pickup_datetime DESC` and `LIMIT {{ var("days_back", 30) }}`
- Update the WHERE clause to `pickup_datetime >= CURRENT_DATE - INTERVAL '{{ var("days_back", 30) }}' DAY`
- Update the WHERE clause to `pickup_datetime >= CURRENT_DATE - INTERVAL '{{ env_var("DAYS_BACK", "30") }}' DAY`
- **Update the WHERE clause to
`pickup_datetime >= CURRENT_DATE - INTERVAL '{{ var("days_back", env_var("DAYS_BACK", "30")) }}' DAY`**
- Update the WHERE clause to
`pickup_datetime >= CURRENT_DATE - INTERVAL '{{ env_var("DAYS_BACK", var("days_back", "30")) }}' DAY`

### Question 3: dbt Data Lineage and Execution

Considering the data lineage below **and** that taxi_zone_lookup is the **only** materialization
build (from a .csv seed file):

![image](./homework_q2.png)

Select the option that does **NOT** apply for materializing `fct_taxi_monthly_zone_revenue`:

- `dbt run`
- `dbt run --select +models/core/dim_taxi_trips.sql+ --target prod`
- `dbt run --select +models/core/fct_taxi_monthly_zone_revenue.sql`
- `dbt run --select +models/core/`
- **`dbt run --select models/staging/+`**

Explanation:

Command `dbt run --select models/staging/+` run all models into staging area.
But `fct_taxi_monthly_zone_revenue` also depend on `dim_zone_lookup` model,
that wont be process at cli command and it will be raise error like this:

```text
08:25:06 Database Error in model hw04_fact_trips (models/core/hw04_fact_trips.sql)
  Not found: Table terraform-probe-448818:zoomcamp.dim_zone_lookup was not found in location europe-west1
  compiled code at target/run/de_zoomcamp_2025_ny_taxi_rides/models/core/hw04_fact_trips.sql
08:25:06 3 of 4 ERROR creating sql table model zoomcamp.hw04_fact_trips ................. [ERROR in 0.40s]
```

### Question 4: dbt Macros and Jinja

Consider you're dealing with sensitive data (e.g.: [PII](https://en.wikipedia.org/wiki/Personal_data)),
that is **only available to your team and very selected few individuals**, in the `raw layer` of your DWH
(e.g: a specific BigQuery dataset or PostgreSQL schema),

- Among other things, you decide to obfuscate/masquerade that data through your staging models,
and make it available in a different schema (a `staging layer`) for other Data/Analytics Engineers to explore

- And **optionally**, yet  another layer (`service layer`), where you'll build your dimension (`dim_`)
and fact (`fct_`) tables (assuming the [Star Schema dimensional modeling](https://www.databricks.com/glossary/star-schema))
for Dashboarding and for Tech Product Owners/Managers

You decide to make a macro to wrap a logic around it:

```sql
{% macro resolve_schema_for(model_type) -%}

    {%- set target_env_var = 'DBT_BIGQUERY_TARGET_DATASET'  -%}
    {%- set stging_env_var = 'DBT_BIGQUERY_STAGING_DATASET' -%}

    {%- if model_type == 'core' -%} {{- env_var(target_env_var) -}}
    {%- else -%}                    {{- env_var(stging_env_var, env_var(target_env_var)) -}}
    {%- endif -%}

{%- endmacro %}
```

And use on your staging, dim_and fact_ models as:

```sql
{{ config(
    schema=resolve_schema_for('core'), 
) }}
```

That all being said, regarding macro above, **select all statements that are true to the models using it**:

- **Setting a value for  `DBT_BIGQUERY_TARGET_DATASET` env var is mandatory, or it'll fail to compile**
- Setting a value for `DBT_BIGQUERY_STAGING_DATASET` env var is mandatory, or it'll fail to compile
- **When using `core`, it materializes in the dataset defined in `DBT_BIGQUERY_TARGET_DATASET`**
- **When using `stg`, it materializes in the dataset defined in `DBT_BIGQUERY_STAGING_DATASET`, or defaults to `DBT_BIGQUERY_TARGET_DATASET`**
- **When using `staging`, it materializes in the dataset defined in `DBT_BIGQUERY_STAGING_DATASET`, or defaults to `DBT_BIGQUERY_TARGET_DATASET`**

## Serious SQL

Alright, in module 1, you had a SQL refresher, so now let's build on top of that with some serious SQL.

These are not meant to be easy - but they'll boost your SQL and Analytics skills to the next level.  
So, without any further do, let's get started...

You might want to add some new dimensions `year` (e.g.: 2019, 2020), `quarter` (1, 2, 3, 4),
`year_quarter` (e.g.: `2019/Q1`, `2019-Q2`), and `month` (e.g.: 1, 2, ..., 12),
**extracted from pickup_datetime**, to your `fct_taxi_trips` OR `dim_taxi_trips.sql`
models to facilitate filtering your queries

### Question 5: Taxi Quarterly Revenue Growth

1. Create a new model `fct_taxi_trips_quarterly_revenue.sql`
2. Compute the Quarterly Revenues for each year for based on `total_amount`
3. Compute the Quarterly YoY (Year-over-Year) revenue growth

- e.g.: In 2020/Q1, Green Taxi had -12.34% revenue growth compared to 2019/Q1
- e.g.: In 2020/Q4, Yellow Taxi had +34.56% revenue growth compared to 2019/Q4

Considering the YoY Growth in 2020, which were the yearly quarters with the best (or less worse)
and worst results for green, and yellow

#### Solving

Into previous model [./dbt/models/core/hw04_fact_trips.sql](dbt/models/core/hw04_fact_trips.sql)
was added axillary fields for extract year, quarter and month entries.

```sql
    ...
    extractedRACT(MONTH FROM trips_unioned.pickup_datetime) as dfreq_month,
    'Q' || EXTRACT(QUARTER FROM trips_unioned.pickup_datetime) as dfreq_quarter,
    EXTRACT(YEAR FROM trips_unioned.pickup_datetime) as dfreq_year
    ...
```

After that was added new model [./dbt/models/core/hw04_dim_taxi_trips_quarterly_revenue.sql](dbt/models/core/hw04_dim_taxi_trips_quarterly_revenue.sql)
for compute quarterly revenue and growth.

- <details>
  <summary>model definition:</summary>

  ```sql
    {{ config(materialized="table") }}

    with
        qrt as (
            select
                fct.service_type,
                fct.dfreq_year,
                fct.dfreq_quarter,
                sum(fct.total_amount) as total_amount
            from {{ ref("hw04_fact_trips") }} as fct
            where extract(year from fct.pickup_datetime) in (2019, 2020)
            group by 1, 2, 3
        ),
        qrt2 as (
            select
                *,
                lag(qrt.total_amount, 4, 0) over (
                    partition by qrt.service_type order by qrt.dfreq_year, qrt.dfreq_quarter
                ) as prev_total_ammount
            from qrt
        )
    select
        -- Revenue grouping 
        dfreq_year as revenue_year,
        dfreq_quarter as revenue_quarter,
        service_type,

        -- Revenue calculation 
        total_amount as cur_total_ammount,
        prev_total_ammount,
        case
            when prev_total_ammount != 0 and total_amount != 0
            then ROUND(((total_amount - prev_total_ammount) / total_amount) * 100, 2)
            else 0
        end as quarter_yty_revenue_growth,
    from qrt2
    order by revenue_year, revenue_quarter, service_type
  ```

</details>

- <details>
  <summary>Result:</summary>

    |revenue_year | revenue_quarter | service_type | cur_total_ammount | prev_total_ammount | quarter_yty_revenue_growth|
    |:----------- | :-------------- | :----------- | :----------------- | :------------------ | :------------------------ |
    |2019 | Q1 | green | 25784959.79 | 0 | 0|
    |2019 | Q1 | yellow | 162985803.33 | 0 | 0|
    |2019 | Q2 | green | 21113088.7 | 0 | 0|
    |2019 | Q2 | yellow | 180235831.11 | 0 | 0|
    |2019 | Q3 | green | 17396258.84 | 0 | 0|
    |2019 | Q3 | yellow | 170539971.73 | 0 | 0|
    |2019 | Q4 | green | 15477249.86 | 0 | 0|
    |2019 | Q4 | yellow | 173180728.59 | 0 | 0|
    |**2020** | **Q1** | **green** | **11469830.44** | **25784959.79** | **-124.81**|
    |**2020** | **Q1** | **yellow** | **142702840.46** | **162985803.33** | **-14.21**|
    |**2020** | **Q2** | **green** | **1545967.08** | **21113088.7** | **-1265.69**|
    |**2020** | **Q2** | **yellow** | **15602926.33** | **180235831.11** | **-1055.14**|
    |2020 | Q3 | green | 2362714.48 | 17396258.84 | -636.28|
    |2020 | Q3 | yellow | 41399509.43 | 170539971.73 | -311.94|
    |2020 | Q4 | green | 2442617.85 | 15477249.86 | -533.63|
    |2020 | Q4 | yellow | 56607021.35 | 173180728.59 | -205.94|

</details>

#### Answers

- green: {best: 2020/Q2, worst: 2020/Q1}, yellow: {best: 2020/Q2, worst: 2020/Q1}
- green: {best: 2020/Q2, worst: 2020/Q1}, yellow: {best: 2020/Q3, worst: 2020/Q4}
- green: {best: 2020/Q1, worst: 2020/Q2}, yellow: {best: 2020/Q2, worst: 2020/Q1}
- **green: {best: 2020/Q1, worst: 2020/Q2}, yellow: {best: 2020/Q1, worst: 2020/Q2}**
- green: {best: 2020/Q1, worst: 2020/Q2}, yellow: {best: 2020/Q3, worst: 2020/Q4}

### Question 6: P97/P95/P90 Taxi Monthly Fare

1. Create a new model `fct_taxi_trips_monthly_fare_p95.sql`
2. Filter out invalid entries (`fare_amount > 0`, `trip_distance > 0`,
and `payment_type_description in ('Cash', 'Credit Card')`)
3. Compute the **continous percentile** of `fare_amount` partitioning by service_type, year and and month

Now, what are the values of `p97`, `p95`, `p90` for Green Taxi and Yellow Taxi, in April 2020?

#### Solving

Was added new model [./dbt/models/core/hw04_dim_taxi_trips_monthly_fare_p95.sql](dbt/models/core/hw04_dim_taxi_trips_monthly_fare_p95.sql)
for compute monthly fare and percentile.

- <details>
  <summary>model definition:</summary>

  ```sql
    {{
        config(
            materialized='table'
        )
    }}

    WITH filtered_trips AS (
        SELECT 
            service_type,
            dfreq_year AS year,
            dfreq_month AS month,
            fare_amount
        FROM {{ ref("hw04_fact_trips") }}
        WHERE 
            fare_amount > 0
            AND trip_distance > 0
            AND payment_type_description IN ('Cash', 'Credit card')
    )

    SELECT DISTINCT
        service_type,
        year as fare_year,
        month as fare_month,
        PERCENTILE_CONT(fare_amount, 0.97) OVER (PARTITION BY service_type, year, month) AS p97,
        PERCENTILE_CONT(fare_amount, 0.95) OVER (PARTITION BY service_type, year, month) AS p95,
        PERCENTILE_CONT(fare_amount, 0.90) OVER (PARTITION BY service_type, year, month) AS p90
    FROM filtered_trips
    ORDER BY fare_year, fare_month, service_type
  ```

</details>

- <details>
  <summary>SQL for get data for solving question:</summary>

  ```sql
  SELECT * FROM `terraform-probe-448818.zoomcamp.hw04_dim_taxi_trips_monthly_fare_p95`
  where fare_year=2020
    and fare_month=4
  ```

- <details>
  <summary>Result:</summary>

  | service_type | fare_year | fare_month | p97 | p95 | p90 |
  |:------------ |:--------- |:---------- |:--- |:--- |:--- |
  | green | 2020 | 4 | 55.0 | 45.0 | 26.5 |
  | yellow | 2020 | 4 | 31.5 | 25.5 | 19.0 |

</details>

#### Answers

- green: {p97: 55.0, p95: 45.0, p90: 26.5}, yellow: {p97: 52.0, p95: 37.0, p90: 25.5}
- **green: {p97: 55.0, p95: 45.0, p90: 26.5}, yellow: {p97: 31.5, p95: 25.5, p90: 19.0}**
- green: {p97: 40.0, p95: 33.0, p90: 24.5}, yellow: {p97: 52.0, p95: 37.0, p90: 25.5}
- green: {p97: 40.0, p95: 33.0, p90: 24.5}, yellow: {p97: 31.5, p95: 25.5, p90: 19.0}
- green: {p97: 55.0, p95: 45.0, p90: 26.5}, yellow: {p97: 52.0, p95: 25.5, p90: 19.0}

### Question 7: Top #Nth longest P90 travel time Location for FHV

Prerequisites:

- Create a staging model for FHV Data (2019), and **DO NOT** add a deduplication step,
just filter out the entries where `where dispatching_base_num is not null`
- Create a core model for FHV Data (`dim_fhv_trips.sql`) joining with `dim_zones`. Similar to what has been done [here](../../../04-analytics-engineering/taxi_rides_ny/models/core/fact_trips.sql)
- Add some new dimensions `year` (e.g.: 2019) and `month` (e.g.: 1, 2, ..., 12),
based on `pickup_datetime`, to the core model to facilitate filtering for your queries

Now...

1. Create a new model `fct_fhv_monthly_zone_traveltime_p90.sql`
2. For each record in `dim_fhv_trips.sql`, compute the [timestamp_diff](https://cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions#timestamp_diff)
in seconds between dropoff_datetime and pickup_datetime - we'll call it `trip_duration` for this exercise
3. Compute the **continous** `p90` of `trip_duration` partitioning by year, month, pickup_location_id, and dropoff_location_id

For the Trips that **respectively** started from `Newark Airport`, `SoHo`, and `Yorkville East`, in November 2019,
what are **dropoff_zones** with the 2nd longest p90 trip_duration ?

#### Solving

- data source `hw04_fhv_raw` added to `staging` schema - which in turn was loaded via Kestra flow (see [./flows/flow.yaml](./flows/flow.yaml))
- intermediate layer for raw data extraction added [w04/dbt/models/staging/hw04_stg_fhv_tripdata.sql](w04/dbt/models/staging/hw04_stg_fhv_tripdata.sql)
- table with facts added [w04/dbt/models/core/hw04_fact_fhv_trips.sql](w04/dbt/models/core/hw04_fact_fhv_trips.sql)
- and in the final stage table with dimensions for solution was added final question [w04/dbt/models/core/hw04_dim_fhv_monthly_zone_traveltime_p90.sql](w04/dbt/models/core/hw04_dim_fhv_monthly_zone_traveltime_p90.sql)

- <details>
  <summary>Final query:</summary>

    ```sql
    with t as (
        SELECT pickup_zone, dropoff_zone, p90,
          ROW_NUMBER() OVER (PARTITION BY pickup_zone ORDER BY p90 desc) AS row_num
        FROM `terraform-probe-448818.zoomcamp.hw04_dim_fhv_monthly_zone_traveltime_p90` 
        where 1=1
          and pickup_zone in (
                'Newark Airport',
                'SoHo',
                'Yorkville East'
              )
          and year = 2019
          and month = 11
    )
    select * from t where row_num = 2
    ORDER BY
        CASE pickup_zone
            WHEN 'Newark Airport' THEN 1
            WHEN 'SoHo' THEN 2
            WHEN 'Yorkville East' THEN 3
            ELSE 4  
        END
    ```

</details>

- <details>
  <summary>Result:</summary>

    | pickup_zone | dropoff_zone | p90 | row_num |
    |:----------- |:------------ |:--- |:------- |
    | Newark Airport | LaGuardia Airport | 7028.81 | 2 |
    | SoHo | Chinatown | 19496.0 | 2 |
    | Yorkville East | Garment District | 13846.0 | 2 |

</details>

#### Answers

- **LaGuardia Airport, Chinatown, Garment District**
- LaGuardia Airport, Park Slope, Clinton East
- LaGuardia Airport, Saint Albans, Howard Beach
- LaGuardia Airport, Rosedale, Bath Beach
- LaGuardia Airport, Yorkville East, Greenpoint

## Submitting the solutions

- Form for submitting: <https://courses.datatalks.club/de-zoomcamp-2025/homework/hw4>

## Solution

- To be published after deadline
