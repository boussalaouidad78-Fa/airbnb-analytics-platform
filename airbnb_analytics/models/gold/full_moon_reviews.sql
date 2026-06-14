{{ config(materialized='table', schema='gold') }}

SELECT
    r.*,
    CASE
        WHEN fm.full_moon_date IS NULL THEN 'not full moon'
        ELSE 'full moon'
    END AS is_full_moon
FROM {{ ref('fact_reviews') }} r
LEFT JOIN {{ ref('seed_full_moon_dates') }} fm
    ON r.review_date = (fm.full_moon_date::DATE + INTERVAL '1 day')