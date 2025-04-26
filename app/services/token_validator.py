import json, os
from urllib.request import urlopen
from jose import jwk, jwt as jose_jwt
from jose.utils import base64url_decode
from datetime import datetime, timezone, timedelta
from app.utils.logger import logger

region = os.getenv("COGNITO_REGION")
user_pool_id = os.getenv("COGNITO_USER_POOL_ID")
issuer = f"https://cognito-idp.{region}.amazonaws.com/{user_pool_id}"
jwks_url = f"{issuer}/.well-known/jwks.json"

def validate_token_remotely(token):
    try:
        headers = jose_jwt.get_unverified_headers(token)
        kid = headers.get('kid')

        with urlopen(jwks_url) as response:
            jwks = json.loads(response.read())
        key = next((k for k in jwks['keys'] if k['kid'] == kid), None)

        if key is None:
            logger.warning("Public key not found in JWKS")
            return {"valid": False, "reason": "invalid_key"}

        public_key = jwk.construct(key)
        message, encoded_sig = token.rsplit('.', 1)
        decoded_sig = base64url_decode(encoded_sig.encode('utf-8'))

        if not public_key.verify(message.encode("utf-8"), decoded_sig):
            logger.warning("Signature verification failed")
            return {"valid": False, "reason": "invalid_signature"}

        claims = jose_jwt.get_unverified_claims(token)
        if claims.get('iss') != issuer or claims.get('token_use') != 'access':
            logger.warning("Invalid token claims")
            return {"valid": False, "reason": "invalid_claims"}

        issued_at = datetime.fromtimestamp(claims['iat'], tz=timezone.utc)
        now = datetime.now(timezone.utc)
        if now - issued_at > timedelta(minutes=5):
            logger.warning("Token expired (older than 5 minutes)")
            return {"valid": False, "reason": "expired"}

        return {"valid": True}

    except Exception as e:
        logger.error(f"JWT validation error: {str(e)}")
        return {"valid": False, "reason": "exception"}
