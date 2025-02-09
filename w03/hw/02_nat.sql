
/*
* Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables.
* What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?
*/
SELECT DISTINCT PULocationID
  FROM terraform-probe-448818.zoomcamp.hw03_native_yellow_tripdata;
