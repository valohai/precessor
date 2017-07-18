def force_bytes(value):
    if isinstance(value, bytes):
        return value
    return str(value).encode('utf-8')
