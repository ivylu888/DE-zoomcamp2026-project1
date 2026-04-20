{{ config(materialized='table') }}

SELECT
    meet_year,
    Sex,
    WeightClassKg,
    MeetCountry,
    Equipment,
    COUNT(*)                        AS total_lifters,
    ROUND(AVG(best_squat_kg), 2)    AS avg_squat_kg,
    ROUND(AVG(best_bench_kg), 2)    AS avg_bench_kg,
    ROUND(AVG(best_deadlift_kg), 2) AS avg_deadlift_kg,
    ROUND(AVG(total_kg), 2)         AS avg_total_kg,
    ROUND(MAX(total_kg), 2)         AS max_total_kg
FROM {{ ref('stg_powerlifting') }}
WHERE meet_year >= 2000
GROUP BY 1,2,3,4,5