# Question 5. Three biggest pickup zones

```sql
/*
Which were the top pickup locations with over 13,000 in total_amount (across all trips) for 2019-10-18?

Consider only lpep_pickup_datetime when filtering by date.

    East Harlem North, East Harlem South, Morningside Heights
    East Harlem North, Morningside Heights
    Morningside Heights, Astoria Park, East Harlem South
    Bedford, East Harlem North, Astoria Park
*/
SELECT
    gt.pu_location_id AS pickup_location,
	tz."zone" as "zone",
    SUM(gt.total_amount) AS total_amount_sum
FROM
    green_tripdata as gt
	LEFT JOIN taxi_zone as tz on tz.location_id=gt.pu_location_id
WHERE
    DATE(gt.lpep_dropoff_datetime) = '2019-10-18'
GROUP BY
    1, 2
HAVING
    SUM(gt.total_amount) >= 13000
ORDER BY
    total_amount_sum DESC;
```

Answer:
```bash
"pickup_location"	"zone"	"total_amount_sum"
74	"East Harlem North"	18732.520000000084
75	"East Harlem South"	16688.81000000007
```