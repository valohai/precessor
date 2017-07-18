from precessor_tests.utils import get_response


def test_netloc_policy():
    response = get_response({'PATH_INFO': '/http://google.com/doggo.jpg'})
    assert response['status'].startswith('403')
    assert response['content'] == b'Netloc google.com not allowed.'


def test_extension_policy():
    response = get_response({'PATH_INFO': '/http://example.com/doggo.png'})
    assert response['status'].startswith('403')
    assert response['content'] == b'Path /doggo.png not allowed.'


def test_scheme_policy():
    response = get_response({'PATH_INFO': '/ftp://example.com/doggo.png'})
    assert response['status'].startswith('403')
    assert response['content'] == b'Invalid URL scheme'
