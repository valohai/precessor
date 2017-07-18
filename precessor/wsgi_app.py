import logging
import traceback

from precessor import config
from precessor.process import process_url
from precessor.util import force_bytes

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
if config.debug:
    logging.getLogger('precessor').setLevel(logging.DEBUG)


def inner_application(environ, start_response):
    url = environ['PATH_INFO'].lstrip('/')
    headers, data = process_url(url, qs=environ.get('QUERY_STRING', ''))
    start_response('200 OK', headers)
    return data


def application(environ, start_response):
    try:
        return inner_application(environ, start_response)
    except Exception as exc:
        content = (traceback.format_exc() if config.debug else str(exc))
        start_response(
            '%d Error' % getattr(exc, 'http_status', 500),
            [('Content-Type', 'text/plain')],
        )
        return force_bytes(content)
