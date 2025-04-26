import psycopg2
import os
from app.utils.logger import logger

# 1. Read database credentials from environment
DB_HOST = os.getenv("RDS_HOST")
DB_NAME = os.getenv("RDS_DB")
DB_USER = os.getenv("RDS_USER")
DB_PASS = os.getenv("RDS_PASSWORD")

# 2. Function to insert file metadata into PostgreSQL
def store_file_metadata(metadata):
    try:
        # 2.1 Connect to the RDS PostgreSQL instance
        print("tejjjjjjjjjjjjjj")
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        cursor = conn.cursor()

        # 2.2 Insert file metadata into the 'file_uploads' table
        cursor.execute("""
            INSERT INTO file_uploads (upload_id, filename, s3_key, timestamp)
            VALUES (%s, %s, %s, %s)
        """, (
            metadata['upload_id'],
            metadata['filename'],
            metadata['s3_key'],
            metadata['timestamp']
        ))

        # 2.3 Commit transaction and close the connection
        conn.commit()
        cursor.close()
        conn.close()
        logger.info("Metadata stored in RDS")

    except Exception as e:
        # 2.4 Log and raise error if storage fails
        logger.error(f"Failed to store metadata in RDS: {str(e)}")
        raise
