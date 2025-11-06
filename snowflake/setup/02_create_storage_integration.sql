// integrations are account level not db/schema level
// Make all setup commands idempotent for pipeline

CREATE STORAGE INTEGRATION IF NOT EXISTS s3_integration
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = 'S3'
  ENABLED = TRUE
  STORAGE_AWS_ROLE_ARN = '${AWS_ROLE_ARN}'
  STORAGE_ALLOWED_LOCATIONS = ('${S3_ALLOWED_LOCATION}')
  COMMENT = 'Snowflake access to raw data bucket';