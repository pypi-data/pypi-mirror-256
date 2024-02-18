import json
import io

import logging
logger = logging.getLogger(__name__)

try:
    import flask
except Exception as e:
    logger.warning(e)

try:
    import marshmallow as m
except Exception as e:
    logger.warning(e)


class RequestSchema(m.Schema):
    class Meta:
        include = {
            'method': m.fields.String(required=True), # TODO: Enumerate
            'path': m.fields.String(required=True),
            'body': m.fields.String(missing=None),
            'type': m.fields.String(missing='text'),
            'seq': m.fields.Integer(required=True),
        }
request_schema = RequestSchema()


def sync_batch_requests():
    # """
    # Execute multiple requests, submitted as a batch.

    # :statuscode 207: Multi status
    # """)
    try:
        request_list = json.loads(flask.request.data)
    except ValueError as e:
        flask.abort(400, str(e))

    # Propagate header from flask.request into exec_request
    #  so authorization tokens, etc can be passed through
    #base_headers = {k:v for k,v in flask.request.headers.to_wsgi_list()}
    base_headers = {
        'Authorization': flask.request.headers.get_all('Authorization'),
        'Content-Type': 'application/json'
    }

    response_list = []
    for idx, req in enumerate(request_list):
        try:
            response = exec_request(req, base_headers)
        except Exception as e:
            response = {
                'status': 500,
                'response': str(e),
            }

        response['seq'] = idx;
        response_list.append(response)

    batch_response = flask.jsonify(response_list)
    return batch_response, 207


def exec_request(req, headers):
    req_dict = request_schema.load(req)

    method = req_dict['method']
    path = req_dict['path']

    # This can't be batched:
    #content_type='application/octet-stream'

    body = req_dict['body']
    content_type = 'application/{}'.format(req_dict['type'])

    app = flask.current_app
    with app.app_context():
        with app.test_request_context(path, method=method, headers=headers, data=body, content_type=content_type):
            try:
                rv = app.preprocess_request()
                if rv is None:
                    rv = app.dispatch_request()
            except Exception as e:
                logger.error(e)
                rv = app.handle_user_exception(e)
            flask_response = app.make_response(rv)
            flask_response = app.process_response(flask_response)
        response = {
            'status': flask_response.status_code,
            'response': convert_response(flask_response)
        }

        return response
    return None


def convert_response(flask_response):
    output = io.StringIO()
    try:
        for line in flask_response.response:
            output.write(line.decode('utf-8'))
        response = output.getvalue()
        try:
            response = json.loads(response)
        except:
            pass
    except Exception as e:
        logger.error('convert_response: {0}'.format(e))
        response = None
    finally:
        output.close()

    return response
