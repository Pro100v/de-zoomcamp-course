{{
    config(
        materialized='table'
    )
}}

WITH tripdata AS (
    SELECT 
        dfreq_year AS year,
        dfreq_month AS month,
        pickup_locationid,
        pickup_zone,
        dropoff_locationid,
        dropoff_zone, 
        TIMESTAMP_DIFF(dropoff_datetime, pickup_datetime, SECOND) AS trip_duration
    FROM {{ ref("hw04_fact_fhv_trips") }}
),
p90_calculation AS (
    SELECT 
        year,
        month,    
        pickup_locationid,
        pickup_zone,
        dropoff_locationid,
        dropoff_zone, 
        -- Calculate the 90th percentile of trip durations
        PERCENTILE_CONT(trip_duration, 0.9) OVER (
            PARTITION BY year, month, pickup_locationid, dropoff_locationid
        ) AS p90
    FROM tripdata
)
-- Финальная агрегация для устранения дубликатов
SELECT 
    year,
    month,
    pickup_locationid,
    pickup_zone,
    dropoff_locationid,
    dropoff_zone,
    MAX(p90) AS p90  -- Или AVG(p90), так как все значения должны быть одинаковыми
FROM p90_calculation
GROUP BY 
    year,
    month,
    pickup_locationid,
    pickup_zone,
    dropoff_locationid,
    dropoff_zone
ORDER BY 
    year, 
    month, 
    pickup_zone, 
    dropoff_zone
