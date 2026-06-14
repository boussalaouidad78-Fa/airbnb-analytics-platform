{{ config(materialized='table', schema='gold') }}

SELECT
    l.listing_id,
    l.listing_name,
    l.room_type,
    l.minimum_nights,
    l.host_id,
    l.price,
    l.created_at,
    h.host_name,
    h.is_superhost
FROM {{ ref('silver_listings') }} l
LEFT JOIN {{ ref('silver_hosts') }} h
    ON l.host_id = h.host_id