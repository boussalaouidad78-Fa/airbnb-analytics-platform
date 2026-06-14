{{ config(materialized='table', schema='silver') }}

SELECT
    id::VARCHAR           AS listing_id,
    listing_url,
    name                  AS listing_name,
    room_type,
    CASE
        WHEN TRY_CAST(minimum_nights AS INT) IS NULL THEN 1
        WHEN TRY_CAST(minimum_nights AS INT) = 0     THEN 1
        ELSE TRY_CAST(minimum_nights AS INT)
    END                   AS minimum_nights,
    host_id::VARCHAR      AS host_id,
    CAST(
        REPLACE(REPLACE(price, '$', ''), ',', '') 
    AS FLOAT)             AS price,
    created_at::TIMESTAMP AS created_at,
    updated_at::TIMESTAMP AS updated_at
FROM {{ ref('bronze_listings') }}
WHERE id IS NOT NULL