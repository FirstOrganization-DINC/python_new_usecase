# ✅ 1. Import required modules and services
from flask import Blueprint, request, jsonify
from app.services.cognito_service import get_cognito_token
from app.utils.logger import logger
from app.services.token_validator import validate_token_remotely

# ✅ 2. Create a Blueprint for auth-related routes
auth_bp = Blueprint('auth', __name__)

# ✅ 3. Define a route to generate token using Cognito
@auth_bp.route('/auth/token', methods=['POST'])
def generate_token():
    try:
        # 3.1 Parse the incoming JSON body
        data = request.get_json()
        client_id = data.get('clientId')
        client_secret = data.get('secret')
        scope = data.get('scope')

        # 3.2 Validate required fields are present
        if not all([client_id, client_secret, scope]):
            logger.warning("Missing one or more required fields: clientId, secret, scope")
            return jsonify({"error": "clientId, secret, and scope are required."}), 400

        # 3.3 Log and call the Cognito token endpoint
        logger.info(f"Received token request for clientId: {client_id}")
        token_response = get_cognito_token(client_id, client_secret, scope)

        # 3.4 Return the generated token to the client
        return jsonify(token_response), 200

    except Exception as e:
        # 3.5 Handle any unexpected errors
        logger.error(f"Error generating token: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500


# ✅ 4. Define a route to validate token against AWS Cognito
@auth_bp.route('/auth/validate', methods=['POST'])
def validate_token():
    try:
        # 4.1 Get the token from the Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid Authorization header"}), 401

        # 4.2 Extract the token from header
        token = auth_header.split(" ")[1]

       

        # 4.4 Validate the token using AWS Cognito JWKS
        if not validate_token_remotely(token):
            return jsonify({"error": "Invalid token"}), 403

        # 4.5 Respond with success if token is valid
        return jsonify({"message": "Token is valid"}), 200

    except Exception as e:
        # 4.6 Log and return error if validation fails
        logger.error(f"Token validation failed: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500
