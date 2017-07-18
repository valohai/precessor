import fnmatch
from urllib.parse import urlparse

import precessor.config as config
from precessor.excs import InvalidUrl


def is_allowed_netloc(netloc):
    return any(fnmatch.fnmatchcase(netloc, allowed_netloc) for allowed_netloc in config.allowed_netlocs)


def is_allowed_path(path):
    if not any(path.endswith(ext) for ext in config.allowed_extensions):
        return False
    return True


def validate_url(url):
    parsed_url = urlparse(url)

    if parsed_url.scheme not in ('http', 'https'):
        raise InvalidUrl('Invalid URL scheme')

    if not is_allowed_netloc(parsed_url.netloc):
        raise InvalidUrl('Netloc %s not allowed.' % parsed_url.netloc)

    if not is_allowed_path(parsed_url.path):
        raise InvalidUrl('Path %s not allowed.' % parsed_url.path)

    return parsed_url
