# Question 6. Largest tip

```sql
/*
For the passengers picked up in October 2019 in the zone named "East Harlem North" which was the drop off zone that had the largest tip?

Note: it's tip , not trip

We need the name of the zone, not the ID.

    Yorkville West
    JFK Airport
    East Harlem North
    East Harlem South
*/
select tz_do."zone", max(gt.tip_amount)
 from green_tripdata as gt
 left join taxi_zone as tz_pu on tz_pu.location_id=gt.pu_location_id
 left join taxi_zone as tz_do on tz_do.location_id=gt.do_location_id
 where gt.lpep_pickup_datetime >= '2019-10-01 00:00:00' and gt.lpep_dropoff_datetime < '2019-11-01 00:00:00'
   and tz_pu."zone"='East Harlem North'
 group by 1
 order by 2 desc
 limit 1
```

Answer:

```bash
"zone"	"max"
"JFK Airport"	87.3
```