-- create native BQ table from external table as data source
CREATE OR REPLACE TABLE terraform-probe-448818.zoomcamp.hw03_native_yellow_tripdata AS
SELECT * FROM `terraform-probe-448818.zoomcamp.hw03_external_yellow_tripdata`
