from functools import wraps
import json
from typing import Dict

import logging
logger = logging.getLogger('')

try:
    import flask
    import redis
    from redis.commands.json.path import Path
except Exception as e:
    logger.warning(e)

from keyrock_encryption import encryption
from . import exc

ALGORITHMS = ["RS256"]
SECRET_KEY = 69
API_KEY_TTL = 36 # 3600

if redis:
    redis = redis.Redis(host='redis', port='6379')


def get_token_auth_header() -> str:
    """
    Obtains the access token from the Authorization Header
    """
    auth = flask.request.headers.get("Authorization", None)
    if not auth:
        raise exc.AuthError({"code": "authorization_header_missing",
                         "description":
                             "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise exc.AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must start with"
                            " Bearer"}, 401)
    if len(parts) == 1:
        raise exc.AuthError({"code": "invalid_header",
                        "description": "Token not found"}, 401)
    if len(parts) > 2:
        raise exc.AuthError({"code": "invalid_header",
                         "description":
                             "Authorization header must be"
                             " Bearer token"}, 401)

    token = parts[1]
    return token


def user_id_to_redis_key(user_id):
    return 'api_key:{}'.format(user_id)


def get_api_token(user_id) -> str:
    """
    Get the existing API token for a user,
     or create a new one
    """
    redis_key = user_id_to_redis_key(user_id)
    if redis.exists(redis_key):
        api_key = redis.get(redis_key).decode()
    else:
        api_key = encryption.get_random_string(16)
        redis.set(redis_key, api_key)

    # Require a new key if unused (requires reloading the page)
    redis.expire(redis_key, API_KEY_TTL)

    # Build the encrypted API Token (includes the random API Key)
    raw_token = {
        'u': user_id,
        'k': api_key
    }
    enc_token = encryption.encrypt_from_json(raw_token, SECRET_KEY)

    return enc_token


def requires_api_token(func):
    """
    Determine if API token is valid
    """
    @wraps(func)
    def decorated(*args, **kwargs):
        is_valid = False

        try:
            enc_token = get_token_auth_header()
            raw_token = encryption.decrypt_to_json(enc_token, SECRET_KEY)

            # Check that the api key matches
            user_id = raw_token['u']
            client_api_key = raw_token['k'].encode()

            server_api_key = redis.get(user_id_to_redis_key(user_id))

            is_valid = client_api_key == server_api_key
        except Exception as e:
            flask.abort(500, str(e))

        if is_valid:
            return func(*args, **kwargs)

        raise exc.AuthError({"code": "invalid_header",
                         "description":
                             "Invalid API token"}, 401)

    return decorated
