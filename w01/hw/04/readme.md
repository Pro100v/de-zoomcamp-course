# Question 4. Longest trip for each day

```sql
/* Which was the pick up day with the longest trip distance? Use the pick up time for your calculations.

Tip: For every day, we only care about one single trip with the longest distance.

    2019-10-11
    2019-10-24
    2019-10-26
    2019-10-31
*/
select cast(gt.lpep_pickup_datetime as date), max(gt.trip_distance)
  from green_tripdata as gt
 where gt.lpep_pickup_datetime::date in ('2019-10-11', '2019-10-24', '2019-10-26', '2019-10-31')
group by 1
order by 2 desc
```

Answer:
```bash
"2019-10-31"	515.89
"2019-10-11"	95.78
"2019-10-26"	91.56
"2019-10-24"	90.75
```