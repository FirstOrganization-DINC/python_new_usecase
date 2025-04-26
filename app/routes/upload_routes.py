from flask import Blueprint, request, jsonify
from app.utils.logger import logger
from app.services.token_validator import validate_token_remotely
from app.utils.s3_util import upload_file_to_s3
from app.utils.rds_util import store_file_metadata
import uuid, datetime

# 1. Create Blueprint for the upload route
upload_bp = Blueprint('upload', __name__)

# 2. Define allowed file types
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

# 3. Helper function to check file extension
def is_allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 4. Upload API endpoint
@upload_bp.route('/upload', methods=['POST'])
def upload_document():
    try:
        # 4.1 Check for Authorization header
        print("heloooo")
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid Authorization header"}), 401

        # 4.2 Extract token from header
        token = auth_header.split(" ")[1]

        # 4.3 Validate token using AWS Cognito
        validation = validate_token_remotely(token)
        if not validation["valid"]:
            if validation["reason"] == "expired":
                return jsonify({"error": "Token expired, please re-authenticate"}), 401
            else:
                return jsonify({"error": "Invalid token"}), 403

        # 4.4 Ensure a file is present in the request
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400


        # 4.5 Extract file from request
        file = request.files['file']

        # 4.6 Check that file is not empty
        file_content = file.read()
        if not file_content:
            return jsonify({"error": "Empty file not allowed"}), 400
        file.seek(0)
        # 4.7 Check that file type is allowed
        if not is_allowed_file(file.filename):
            return jsonify({"error": "Only PDF, DOC, and TXT formats allowed"}), 400

        # 4.8 Generate a timestamped S3 key
        timestamp = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')
        s3_key = f"uploads/{timestamp}_{file.filename}"

        # 4.9 Upload the file to S3
        upload_file_to_s3(file, s3_key)

        # 4.10 Generate a unique ID for this upload
        upload_id = str(uuid.uuid4())

        #4.11 Prepare and store metadata in RDS
        metadata = {
            "upload_id": upload_id,
            "filename": file.filename,
            "s3_key": s3_key,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
        store_file_metadata(metadata)

        # 4.12 Respond with success and upload ID
        return jsonify({"message": "File uploaded successfully", "upload_id": upload_id}), 200

    except Exception as e:
        # 4.13 Log and return internal error
        logger.error(f"Error during file upload: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500
