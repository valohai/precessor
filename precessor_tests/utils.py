import os
from wsgiref.util import setup_testing_defaults

import requests_mock

from precessor import application

with open(os.path.join(os.path.dirname(__file__), 'niMh7MJ.jpg'), 'rb') as doggo_fp:
    doggo_data = doggo_fp.read()


def get_response(environ):
    response = {}
    setup_testing_defaults(environ)
    with requests_mock.mock() as m:
        m.get('http://example.com/doggo.jpg', content=doggo_data)
        response['content'] = application(
            environ,
            start_response=lambda status, headers: response.update({'status': status, 'headers': headers}),
        )
    return response
