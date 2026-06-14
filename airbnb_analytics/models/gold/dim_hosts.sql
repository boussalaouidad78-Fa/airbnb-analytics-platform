{{ config(materialized='table', schema='gold') }}

SELECT
    host_id,
    COALESCE(host_name, 'Anonymous') AS host_name,
    is_superhost,
    created_at,
    updated_at
FROM {{ ref('silver_hosts') }}
