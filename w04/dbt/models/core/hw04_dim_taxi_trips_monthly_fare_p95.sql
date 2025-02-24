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
