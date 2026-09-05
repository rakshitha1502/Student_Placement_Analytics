{% snapshot company_snapshot %}

{{
config(
target_schema='ANALYTICS',
unique_key='COMPANY_ID',
strategy='check',
check_cols=[
'COMPANY_NAME',
'INDUSTRY',
'HQ_COUNTRY',
'SIZE_BAND',
'HIRING_CITY',
'HIRING_STATE',
'STATUS'
]
)
}}

SELECT
COMPANY_ID,
COMPANY_NAME,
INDUSTRY,
HQ_COUNTRY,
SIZE_BAND,
HIRING_CITY,
HIRING_STATE,
STATUS
FROM STUDENT_PLACEMENT_DB.RAW.RAW_COMPANIES

{% endsnapshot %}
