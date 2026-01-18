# Answers to the homework #1

## Question 1
**What's the version of pip in the python:3.13 image? (1 point)**
```sh
docker run --rm python:3.13 pip --version
```

Answer: `25.3`


## Question 2
**Given the docker-compose.yaml, what is the hostname and port that pgadmin should use to connect to the postgres database? (1 point)**

Answer: `db:5432`


## Question 3
**For the trips in November 2025, how many trips had a trip_distance of less than or equal to 1 mile? (1 point)**
```sql
SELECT count(1) FROM green_taxi_trips
WHERE trip_distance <= 1
AND lpep_pickup_datetime >= '2025-11-01' AND lpep_pickup_datetime < '2025-12-01'
```
Answer: `8007`


## Question 4
**Which was the pick up day with the longest trip distance? Only consider trips with trip_distance less than 100 miles. (1 point)**
```sql
SELECT lpep_pickup_datetime
FROM green_taxi_trips
WHERE trip_distance = (SELECT max(trip_distance)
                       FROM green_taxi_trips WHERE trip_distance < 100)
```

Answer: `2025-11-14`


## Question 5
**Which was the pickup zone with the largest total_amount (sum of all trips) on November 18th, 2025? (1 point)**
```sql
SELECT
    z."Zone",
    SUM(t.total_amount) AS sum_total_amount
FROM green_taxi_trips AS t
JOIN zones AS z
ON t."PULocationID" = z."LocationID"
WHERE t.lpep_pickup_datetime::date = '2025-11-18'
GROUP BY z."Zone"
ORDER BY sum_total_amount DESC
LIMIT 1;
```

Answer: `East Harlem North`


## Question 6
**For the passengers picked up in the zone named "East Harlem North" in November 2025, which was the drop off zone that had the largest tip? (1 point)**
```sql
SELECT
    z_drop."Zone" AS dropoff_zone,
    t.tip_amount
FROM green_taxi_trips AS t
JOIN zones AS z_pick
ON t."PULocationID" = z_pick."LocationID"
JOIN zones AS z_drop
ON t."DOLocationID" = z_drop."LocationID"
WHERE z_pick."Zone" = 'East Harlem North'
AND t.lpep_pickup_datetime >= '2025-11-01'
AND t.lpep_pickup_datetime < '2025-12-01'
ORDER BY t.tip_amount DESC
LIMIT 1;
```

Answer: `Yorkville West`


## Question 7
**Which of the following sequences describes the Terraform workflow for: 1) Downloading plugins and setting up backend, 2) Generating and executing changes, 3) Removing all resources? (1 point)**

Answer: `terraform init, terraform apply -auto-approve, terraform destroy`
