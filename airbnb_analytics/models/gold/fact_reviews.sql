{{ config(materialized='table', schema='gold') }}

SELECT *
FROM {{ ref('silver_reviews') }}
WHERE review_text IS NOT NULL
ORDER BY review_date DESC