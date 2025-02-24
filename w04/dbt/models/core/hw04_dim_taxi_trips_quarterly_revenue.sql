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
