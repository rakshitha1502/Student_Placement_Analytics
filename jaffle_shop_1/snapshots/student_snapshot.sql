{% snapshot student_snapshot %}

{{
config(
target_schema='ANALYTICS',
unique_key='STUDENT_ID',
strategy='check',
check_cols=[
'FIRST_NAME',
'LAST_NAME',
'GENDER',
'PROGRAM',
'BRANCH',
'GRAD_YEAR',
'CGPA',
'SEGMENT',
'COLLEGE_ID'
]
)
}}

SELECT
STUDENT_ID,
FIRST_NAME,
LAST_NAME,
GENDER,
PROGRAM,
BRANCH,
GRAD_YEAR,
CGPA,
SEGMENT,
COLLEGE_ID
FROM STUDENT_PLACEMENT_DB.RAW.RAW_STUDENTS

{% endsnapshot %}
