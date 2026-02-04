# Answers to the homework #3

## Question 1. Counting records
**What is count of records for the 2024 Yellow Taxi Data? (1 point)**
```sql
SELECT count(*)
FROM kestra-sandbox-485717.zoomcamp.yellow_tripdata_non_partitioned;
```

Answer: `20,332,093`


## Question 2. Data read estimation
**Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables. What is the estimated amount of data that will be read when this query is executed on the External Table and the Table? (1 point)**
```sql
SELECT COUNT(DISTINCT PULocationID)
FROM kestra-sandbox-485717.zoomcamp.external_yellow_tripdata;
```

Answer: `0 MB for the External Table and 155.12 MB for the Materialized Table`


## Question 3. Understanding columnar storage
**Write a query to retrieve the PULocationID from the table (not the external table) in BigQuery. Now write a query to retrieve the PULocationID and DOLocationID on the same table. Why are the estimated number of Bytes different? (1 point)**
```sql
SELECT PULocationID FROM kestra-sandbox-485717.zoomcamp.yellow_tripdata_non_partitioned;

SELECT PULocationID, DOLocationID FROM kestra-sandbox-485717.zoomcamp.yellow_tripdata_non_partitioned;
```

Answer: `BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns requires reading more data than querying one column.`


## Question 4. Counting zero fare trips
**How many records have a fare_amount of 0? (1 point)**
```sql
SELECT COUNT(*)
FROM kestra-sandbox-485717.zoomcamp.yellow_tripdata_non_partitioned
WHERE fare_amount = 0;
```

Answer: `8333`


## Question 5. Partitioning and clustering
**What is the best strategy to make an optimized table in Big Query if your query will always filter based on tpep_dropoff_datetime and order the results by VendorID (Create a new table with this strategy) (1 point)**

Answer: `Partition by tpep_dropoff_datetime and Cluster on VendorID`


## Question 6. Partition benefits
**Write a query to retrieve the distinct VendorIDs between tpep_dropoff_datetime 2024-03-01 and 2024-03-15 (inclusive). Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 5 and note the estimated bytes processed. What are these values? Choose the answer which most closely matches. (1 point)**

```sql
CREATE OR REPLACE TABLE kestra-sandbox-485717.zoomcamp.yellow_tripdata_partitioned_clustered
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS
SELECT * FROM kestra-sandbox-485717.zoomcamp.external_yellow_tripdata;

SELECT DISTINCT VendorID
FROM kestra-sandbox-485717.zoomcamp.yellow_tripdata_non_partitioned
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';

SELECT DISTINCT VendorID
FROM kestra-sandbox-485717.zoomcamp.yellow_tripdata_partitioned_clustered
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';
```

Answer: `310.24 MB for non-partitioned table and 26.84 MB for the partitioned table`


## Question 7. External table storage
**Where is the data stored in the External Table you created? (1 point)**

Answer: `GCP Bucket`

## Question 8. Clustering best practices
**It is best practice in Big Query to always cluster your data: (1 point)**

Answer: `False`

## Question 9. Understanding table scans
**No Points: Write a SELECT count(*) query FROM the materialized table you created. How many bytes does it estimate will be read? Why?**
```sql
SELECT count(*) FROM `kestra-sandbox-485717.zoomcamp.yellow_tripdata_non_partitioned`;
```

Answer: `0 B`.
BigQuery stores table metadata so there's no need to scan the whole table.
