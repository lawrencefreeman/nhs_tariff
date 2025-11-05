 integrations are account level not db/schema level
// Make all setup commands idempotent for pipeline

CREATE STORAGE INTEGRATION IF NOT EXISTS s3_integration
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = 'S3'
  ENABLED = TRUE
  STORAGE_AWS_ROLE_ARN = '{{ env_var("AWS_ROLE_ARN") }}'
  STORAGE_ALLOWED_LOCATIONS = ('{{ env_var("S3_ALLOWED_LOCATION") }}')
  COMMENT = 'Snowflake access to raw data bucket';

  
// confirm the creation of the integration and extract AWS details to setup the IAM trust policy
// The following myst be retrieved and embedded into AWS policy:
// STORAGE_AWS_IAM_USER_ARN
// STORAGE_AWS_EXTERNAL_ID

DESC INTEGRATION s3_integration;
