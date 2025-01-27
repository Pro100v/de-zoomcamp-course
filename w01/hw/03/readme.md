# Question 3. Trip Segmentation Count

```sql
/* During the period of October 1st 2019 (inclusive) and November 1st 2019 (exclusive), how many trips, respectively, happened:
    Up to 1 mile
    In between 1 (exclusive) and 3 miles (inclusive),
    In between 3 (exclusive) and 7 miles (inclusive),
    In between 7 (exclusive) and 10 miles (inclusive),
    Over 10 miles
*/
select '1', count(1), 'Up to 1 mile' from green_tripdata as gt
 where gt.lpep_pickup_datetime >= '2019-10-01 00:00:00' and gt.lpep_dropoff_datetime < '2019-11-01 00:00:00'
   and gt.trip_distance <= 1
union  
select '2', count(1), 'In between 1 (exclusive) and 3 miles (inclusive)' from green_tripdata as gt
 where gt.lpep_pickup_datetime >= '2019-10-01 00:00:00' and gt.lpep_dropoff_datetime < '2019-11-01 00:00:00'
   and gt.trip_distance > 1 and gt.trip_distance <= 3
union  
select '3', count(1), 'In between 3 (exclusive) and 7 miles (inclusive)' from green_tripdata as gt
 where gt.lpep_pickup_datetime >= '2019-10-01 00:00:00' and gt.lpep_dropoff_datetime < '2019-11-01 00:00:00'
   and gt.trip_distance > 3 and gt.trip_distance <= 7
union  
select '4', count(1), 'In between 7 (exclusive) and 10 miles (inclusive)' from green_tripdata as gt
 where gt.lpep_pickup_datetime >= '2019-10-01 00:00:00' and gt.lpep_dropoff_datetime < '2019-11-01 00:00:00'
   and gt.trip_distance > 7 and gt.trip_distance <= 10
union  
select '5', count(1), 'Over 10 miles' from green_tripdata as gt
 where gt.lpep_pickup_datetime >= '2019-10-01 00:00:00' and gt.lpep_dropoff_datetime < '2019-11-01 00:00:00'
   and gt.trip_distance > 10
```

Answer:
```bash
"1"	104802	"Up to 1 mile"
"2"	198924	"In between 1 (exclusive) and 3 miles (inclusive)"
"3"	109603	"In between 3 (exclusive) and 7 miles (inclusive)"
"4"	27678	"In between 7 (exclusive) and 10 miles (inclusive)"
"5"	35189	"Over 10 miles"
```