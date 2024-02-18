import logging
logger = logging.getLogger(__name__)

from typing import Dict

try:
    import flask
except Exception as e:
    logger.warning(e)


# Format error response and append status code.
class AuthError(Exception):
    """
    An AuthError is raised whenever the authentication failed.
    """
    def __init__(self, error: Dict[str, str], status_code: int):
        super().__init__()
        self.error = error
        self.status_code = status_code


def attach_error_handlers(app):
    app.errorhandler(AuthError)(handle_auth_error)


def handle_auth_error(ex: AuthError) -> flask.Response:
    """
    serializes the given AuthError as json and sets the response status code accordingly.
    :param ex: an auth error
    :return: json serialized ex response
    """
    response = flask.jsonify(ex.error)
    response.status_code = ex.status_code
    return response
