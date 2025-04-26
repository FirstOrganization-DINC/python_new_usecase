-- ✅ Create table to store uploaded file metadata

CREATE TABLE IF NOT EXISTS file_uploads (
    upload_id UUID PRIMARY KEY,             -- Unique ID for each upload
    filename TEXT NOT NULL,                 -- Original file name
    s3_key TEXT NOT NULL,                   -- S3 object key
    timestamp TIMESTAMP NOT NULL            -- Upload time (UTC)
);
