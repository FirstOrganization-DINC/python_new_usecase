import requests
import os
from app.utils.logger import logger

# 1. Function to request an OAuth token from AWS Cognito
def get_cognito_token(client_id, client_secret, scope):
    try:
        # 1.1 Prepare URL and headers
        print("heloo")
        # url = os.getenv("COGNITO_TOKEN_URL")
        url="https://us-east-1dufobtsjb.auth.us-east-1.amazoncognito.com/oauth2/token"
        print(url)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        # 1.2 Build request body
        body = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": scope
        }

        # 1.3 Call Cognito token endpoint
        logger.info(f"Requesting token from Cognito for clientId: {client_id}")
        response = requests.post(url, data=body, headers=headers)

        # 1.4 Return token if successful
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Token request failed", "details": response.text}

    except Exception as e:
        # 1.5 Handle exception during token request
        logger.error(f"Error calling Cognito for token: {str(e)}")
        return {"error": "Internal error"}
