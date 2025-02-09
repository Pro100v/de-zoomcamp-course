CREATE OR REPLACE TABLE terraform-probe-448818.zoomcamp.hw03_05_native_yellow_tripdata
  PARTITION BY DATE(tpep_dropoff_datetime)
  CLUSTER BY VendorID
  AS
  SELECT * FROM terraform-probe-448818.zoomcamp.hw03_external_yellow_tripdata
