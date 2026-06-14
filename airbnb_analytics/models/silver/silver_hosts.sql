{{ config(materialized='table', schema='silver') }}

SELECT
    id::VARCHAR        AS host_id,
    name               AS host_name,
    CASE 
        WHEN is_superhost = 't' THEN TRUE
        WHEN is_superhost = 'true' THEN TRUE
        ELSE FALSE
    END                AS is_superhost,
    created_at::TIMESTAMP AS created_at,
    updated_at::TIMESTAMP AS updated_at
FROM {{ ref('bronze_hosts') }}
WHERE id IS NOT NULL