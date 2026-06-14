{{ config(materialized='view', schema='bronze') }}

SELECT * 
FROM read_csv_auto('../data/hosts.csv')