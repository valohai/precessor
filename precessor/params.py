from precessor.excs import InvalidParameter

default_params = {
    'quality': 75,
    'format': 'jpeg',
}

format_to_mime = {
    'jpeg': 'image/jpeg',
    'png': 'image/png',
}


def parse_params(qs):
    params = default_params.copy()
    operation_qs = []
    for param, value in qs:
        if param in params:
            params[param] = value
        else:
            operation_qs.append((param, value))

    if params['format'] not in ('png', 'jpeg'):
        raise InvalidParameter('invalid format %s' % params['format'])

    try:
        params['quality'] = int(params['quality'])
        assert 1 <= params['quality'] <= 100
    except:
        raise InvalidParameter('invalid quality %s' % params['quality'])

    return (params, operation_qs)
