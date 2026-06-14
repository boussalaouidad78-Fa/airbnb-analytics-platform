{{ config(materialized='table', schema='silver') }}

SELECT
    listing_id::VARCHAR AS listing_id,
    date::DATE          AS review_date,
    reviewer_name,
    comments            AS review_text,
    sentiment
FROM {{ ref('bronze_reviews') }}
WHERE comments IS NOT NULL