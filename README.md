precessor – an image processor proxy
====================================

Installation
------------

Precessor is a Python 3 WSGI application, so you'll need a WSGI server.
uWSGI is recommended and tested and will be used throughout the readme.

Precessor uses `memcache` as its cache. Although it's not strictly required, you're probably going to have
a bad time without `memcache`. Also, it's recommended that you configure `memcache` for large values; by default,
`memcache` limits values to 1 MiB, and input images (which are also cached) can easily be larger.
The `-I` command line parameter to `memcached` controls this: `memcached -m 1024 -I 32m`, for instance.

First install `precessor` and its requirements in a virtualenv (as you do).

Configure by setting environment variables:

* `DEBUG`: whether to show tracebacks and log more
* `MEMCACHED_SERVERS`: Memcached host:port pairs, separated by commas. Defaults to `127.0.0.1:11211`.
* `MEMCACHED_PREFIX`: Prefix for Memcached keys. Defaults to none.
* `ALLOWED_NETLOCS`: Allowed netlocs (domains) for proxied images, separated by commas. May be wildcard patterns.
* `ALLOWED_EXTENSIONS`: Allowed extensions for proxied images, separated by commas. Defaults to `jpg,jpeg,png,gif`.

Then run the app – for instance, you can do this with uWSGI:

```bash
$ uwsgi --wsgi=precessor --http=:8000 --virtualenv=$VIRTUAL_ENV '--env=ALLOWED_NETLOCS=*.imgur.com'
```

Usage
-----

Let's start with some examples.

Assuming Precessor is running on `http://localhost:8000/` and allows proxying imgur.com, we're
going to be processing [this silly doggo](https://i.imgur.com/niMh7MJ.jpg).

* `http://localhost:8000/https://i.imgur.com/niMh7MJ.jpg`
   – just re-encode the doggo to JPEG at default settings.
* `http://localhost:8000/https://i.imgur.com/niMh7MJ.jpg?resize=800x`
   – resize the doggo to be 800 px wide.
* `http://localhost:8000/https://i.imgur.com/niMh7MJ.jpg?resize=100x300`
   – resize the doggo to be exactly 100x300 px.
* `http://localhost:8000/https://i.imgur.com/niMh7MJ.jpg?rotate=90&resize=100x`
   – rotate the doggo 90 degrees, then resize to 100 px wide.
* `http://localhost:8000/https://i.imgur.com/niMh7MJ.jpg?resize=100x&rotate=90`
   – resize the doggo to 100 px wide, then rotate by 90 degrees.
* `http://localhost:8000/https://i.imgur.com/niMh7MJ.jpg?resize=100x&quality=30`
   – resize the doggo to 100 px wide, output a quality 30 JPEG.
   
Operations
----------

Operations are run in sequence, as they are encountered in the query string.

### `resize=WxH[,mode]` (and `resize-larger` and `resize-smaller`)

Resize the image to W x H pixels.

You can optionally set a quality mode (`nearest`/`bilinear`/`bicubic`/`lanczos`),
which defaults to the best quality (`lanczos`).

If either the W or H parameter is elided, it will be automatically calculated based on the input image's aspect ratio.

`resize-larger` and `resize-smaller` are no-ops if the source image is larger or smaller, respectively,
than the requested size.

### `flip=[x][y]`

Flip the image along the X ("mirror") or Y ("flip") axes.

### `rotate=angle`

Rotate the image by `angle` degrees.

Parameters
----------

In addition to operations, as described above, there's a couple of global parameters that define the output format:

* `quality`: JPEG quality (0-100)
* `format`: `jpeg` (default) or `png`.

These can appear at any point in the query string.
