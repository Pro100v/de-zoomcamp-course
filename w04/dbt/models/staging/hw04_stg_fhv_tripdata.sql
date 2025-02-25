{{
    config(
        materialized='view'
    )
}}

with
    tripdata as (
        select *
        from {{ source("staging", "hw04_fhv_raw") }}
        where dispatching_base_num is not null
    )
select 
    -- identifiers / идентификаторы
    {{ dbt_utils.generate_surrogate_key(['dispatching_base_num', 'pickup_datetime']) }} as hire_id,
    dispatching_base_num,
    -- timestamps / временные метки
    cast(pickup_datetime as timestamp) as pickup_datetime,
    cast(dropOff_datetime as timestamp) as dropoff_datetime,
    -- identifiers / идентификаторы
    {{ dbt.safe_cast("PUlocationID", api.Column.translate_type("integer")) }} as pickup_locationid,
    {{ dbt.safe_cast("DOlocationID", api.Column.translate_type("integer")) }} as dropoff_locationid,
    {{ dbt.safe_cast("SR_Flag", api.Column.translate_type("integer")) }} as sr_flag,
    Affiliated_base_number as affiliated_base_number
from tripdata
where 1 = 1
-- dbt build --select <model-name> --vars '{'is_test_run': 'false'}'
{% if var("is_test_run", default=true) %} limit 100 {% endif %}