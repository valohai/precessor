import pylibmc

import precessor.config as config

pool = pylibmc.ClientPool(pylibmc.Client(servers=config.memcached_servers, binary=True), 4)

ignorable_errors = (pylibmc.ServerDown, pylibmc.ConnectionError)


def get(key):
    if not config.cache_enabled:
        return None
    try:
        with pool.reserve() as cache:
            return cache.get('%s%s' % (config.memcached_prefix, key))
    except ignorable_errors:
        return None


def set(key, value):
    if not config.cache_enabled:
        return None
    try:
        with pool.reserve() as cache:
            return cache.set('%s%s' % (config.memcached_prefix, key), value)
    except ignorable_errors:
        return None
