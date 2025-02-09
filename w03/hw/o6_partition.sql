SELECT DISTINCT VendorID 
  FROM terraform-probe-448818.zoomcamp.hw03_05_native_yellow_tripdata
  where tpep_dropoff_datetime between '2024-03-01' and '2024-03-15';
