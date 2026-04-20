{{ config(materialized='view') }}

SELECT
    Name,
    Sex,
    Equipment,
    Age,
    BodyweightKg,
    WeightClassKg,
    CAST(Best3SquatKg AS FLOAT64)   AS best_squat_kg,
    CAST(Best3BenchKg AS FLOAT64)   AS best_bench_kg,
    CAST(Best3DeadliftKg AS FLOAT64) AS best_deadlift_kg,
    CAST(TotalKg AS FLOAT64)        AS total_kg,
    CAST(Dots AS FLOAT64)           AS dots_score,
    Place,
    Federation,
    MeetCountry,
    CAST(Date AS DATE)              AS meet_date,
    EXTRACT(YEAR FROM CAST(Date AS DATE)) AS meet_year
FROM {{ source('powerlifting_data', 'raw_powerlifting') }}
WHERE TotalKg IS NOT NULL
  AND Date IS NOT NULL