USE DATABASE NHS_TARIFF_DEV;
USE SCHEMA BRONZE;

CREATE TABLE IF NOT EXISTS BRONZE.ICD10_RAW (
    CODE                STRING,         -- e.g. A00.0
    ALT_CODE            STRING,         -- A000X
    USAGE               STRING,         -- 'DAGGER', 'ASTERISK', etc.
    USAGE_UK            NUMBER(1,0),
    DESCRIPTION         STRING,
    MODIFIER_4          STRING,
    MODIFIER_5          STRING,
    QUALIFIERS          STRING,
    GENDER_MASK         NUMBER(1,0),
    MIN_AGE             NUMBER(3,0),
    MAX_AGE             NUMBER(3,0),
    TREE_DESCRIPTION    STRING,
    LOAD_TS             TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);



COPY INTO BRONZE.ICD10_RAW
FROM @bronze_raw_stage/ICD10/
FILE_FORMAT = (FORMAT_NAME = TXT_ICD10_FORMAT ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE)
ON_ERROR = 'CONTINUE'
PURGE = FALSE // do not clean out source files on success
FORCE = FALSE; // do not force overwrite, enable idempotent as by detault