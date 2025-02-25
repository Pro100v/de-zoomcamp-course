{{
    config(
        materialized='table'
    )
}}

with fhv_tripdata as (
    select *
    from {{ ref('hw04_stg_fhv_tripdata') }}
),
dim_zones as (
    select * 
    from {{ ref('hw04_dim_zones') }}
    where borough != 'Unknown'
)
select 
    fhv_tripdata.hire_id, 
    fhv_tripdata.dispatching_base_num,
    fhv_tripdata.pickup_datetime,
    fhv_tripdata.pickup_locationid,
    pickup_zone.borough as pickup_borough, 
    pickup_zone.zone as pickup_zone, 
    fhv_tripdata.dropoff_datetime,
    fhv_tripdata.dropoff_locationid,
    dropoff_zone.borough as dropoff_borough, 
    dropoff_zone.zone as dropoff_zone,  
    fhv_tripdata.sr_flag,
    fhv_tripdata.affiliated_base_number,
    EXTRACT(MONTH FROM fhv_tripdata.pickup_datetime) as dfreq_month,
    'Q' || EXTRACT(QUARTER FROM fhv_tripdata.pickup_datetime) as dfreq_quarter,
    EXTRACT(YEAR FROM fhv_tripdata.pickup_datetime) as dfreq_year    
from fhv_tripdata
inner join dim_zones as pickup_zone
        on fhv_tripdata.pickup_locationid = pickup_zone.locationid
inner join dim_zones as dropoff_zone
        on fhv_tripdata.dropoff_locationid = dropoff_zone.locationid
order by fhv_tripdata.pickup_datetime