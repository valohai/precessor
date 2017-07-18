import os

debug = bool(int(os.environ.get('DEBUG', '0')))
memcached_servers = list(os.environ.get('MEMCACHED_SERVERS', '127.0.0.1:11211').split(','))
memcached_prefix = os.environ.get('MEMCACHED_PREFIX', '')
allowed_netlocs = set(os.environ.get('ALLOWED_NETLOCS', 'none').split(','))
allowed_extensions = set('.%s' % ext for ext in os.environ.get('ALLOWED_EXTENSIONS', 'jpg,jpeg,png,gif').split(','))
cache_enabled = True
