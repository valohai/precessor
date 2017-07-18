import hashlib
import logging
from io import BytesIO
from urllib.parse import parse_qsl

import requests
from PIL import Image

from precessor import cache
from precessor.ops import parse_operations
from precessor.params import parse_params, format_to_mime
from precessor.policy import validate_url
from precessor.timing import Timer
from precessor.util import force_bytes

log = logging.getLogger(__name__)


def get_url_data(url, url_cache_key):
    data = cache.get(url_cache_key)
    if data:
        log.debug('URL CACHE HIT for URL %s' % url)
        return data
    log.debug('URL CACHE MISS for URL %s' % url)
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.content
    cache.set(url_cache_key, data)
    return data


def process_url(url, qs):
    timer = Timer()
    timer.save_time('start')
    validate_url(url)
    params, operation_qs = parse_params(parse_qsl(qs))

    # The convoluted cache keying allows users to shift quality/format parameters around
    # and still get the same cached result.

    url_cache_key = 'url=%s' % hashlib.md5(force_bytes(url)).hexdigest()
    params_cache_key = 'params=%s' % hashlib.md5(force_bytes(list(sorted(params.items())))).hexdigest()
    ops_cache_key = 'ops=%s' % hashlib.md5(force_bytes(operation_qs)).hexdigest()
    cache_key = '%s,%s,%s' % (url_cache_key, params_cache_key, ops_cache_key)

    cache_entry = cache.get(cache_key)
    if cache_entry:
        log.debug('RESULT CACHE HIT for URL %s, qs %s', url, qs)
        return cache_entry
    log.debug('RESULT CACHE MISS for URL %s, qs %s', url, qs)

    operations = parse_operations(operation_qs)
    timer.save_time('operations parsed')
    data = get_url_data(url, url_cache_key)
    timer.save_time('url retrieved')

    image = Image.open(BytesIO(data))
    for op in operations:
        image = op.process(image)
        timer.save_time('operation %s executed' % op)

    bio = BytesIO()
    image.save(bio, format=params['format'], quality=params['quality'])
    timer.save_time('image serialized')
    data = bio.getvalue()
    headers = [
        ('Content-Type', format_to_mime[params['format']]),
        ('Content-Length', str(len(data))),
    ]
    cache.set(cache_key, (headers, data))
    timer.save_time('done')
    log.info(
        'URL %s, params %s; processing took %d msec:\n%s',
        url, params, timer.total_duration * 1000, '\n'.join(timer.get_summary())
    )
    return (headers, data)
